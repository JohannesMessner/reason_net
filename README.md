# ReasonNet


## generate data (for data-100m.txt)

```bash
cd data_gen
cargo run --release -- --min 3 --max 5 --size 25000000 --seed 32 --save-file-path data-25m-add.txt
mv data-25m-add.txt ../datasets/.


cargo run --release -- --min 3 --max 5 --size 100000000 --seed 32 --save-file-path data-100m-all.txt
mv data-100m-all.txt ../datasets/.

```

For the addition grokking run:

```bash
 cargo run --release -- --min 4 --max 5 --size 7000 --seed 32 --save-file-path data-grokking-addition.txt --operators +
mv data-grokking-addition.txt ../datasets/.
```


## run the training


normal 

```bash
python reason_net/run.py --config-path configs --config-name all-14m.yaml
```


reason middle

```bash
python reason_net/run.py --config-path configs --config-name all-14m.yaml reason_mode=true 
```


reason left 
```bash
python reason_net/run.py --config-path configs --config-name all-14m.yaml reason_mode=true +data.reason.reason_token_pos="left" 
```


With small model for test

```bash
python reason_net/run.py --config-path configs --config-name all-14m.yaml module/model=910K
```

addition grokking:

```bash
python reason_net/run.py --config-path configs --config-name grokking-addition.yaml
```
