from pathlib import Path
from omegaconf import DictConfig, open_dict
import pytest
import torch

from reason_net.run import run, omegaconf_to_pydantic
from reason_net.generate import generate
from hydra import compose, initialize


def raw_config() -> DictConfig:
    with initialize(
        version_base=None,
        config_path="../reason_net/configs",
    ):
        raw_conf = compose(config_name="all-14m.yaml", overrides=["module/model=910K"])

    return raw_conf


def _init_config(cfg: DictConfig) -> DictConfig:
    with open_dict(cfg):
        cfg.trainer.pl.max_epochs = 2
        cfg.data.num_workers = 0
        cfg.wandb.enabled = False
        cfg.data.dataset_path = Path("tests/data-test.txt")

        cfg.trainer.callbacks = {
            "norm_monitor": {"log_every_n_steps": 1},
        }

    return cfg


def normal_config() -> DictConfig:
    raw_conf = _init_config(raw_config())
    config = omegaconf_to_pydantic(raw_conf)

    config.reason_mode = False
    return config


def reason_middle_config() -> DictConfig:
    raw_conf = _init_config(raw_config())
    config = omegaconf_to_pydantic(raw_conf)

    config.reason_mode = True
    config.data.reason.reason_token_pos = "middle"  # type: ignore
    return config


def reason_left_config() -> DictConfig:
    raw_conf = _init_config(raw_config())
    config = omegaconf_to_pydantic(raw_conf)

    config.reason_mode = True
    config.data.reason.reason_token_pos = "left"  # type: ignore
    return config


@pytest.mark.parametrize(
    "config", [normal_config(), reason_middle_config(), reason_left_config()]
)
def test_run(config: DictConfig, tmp_path: Path):
    config.trainer.save_dir = tmp_path

    module, data = run(config)

    if torch.cuda.is_available():
        module.to("cuda")

    idx = torch.Tensor(data.tokenizer.encode("1+1")).long().to(module.device)
    generated = generate(module.model, idx, 10).to("cpu").tolist()
    decoded = data.tokenizer.decode(generated)

    assert decoded is not None
