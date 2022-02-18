## Qi Dao vault optimizer

## Prequisites

* python 3.9
* eth-brownie 1.17.2
* python3-env


## Steps to install

### Install python virtual environent

```bash 
python -m venv .venv
```

### Activate virtual environment
```bash
source .venv/bin/activate
```

### Install requirements
```bash
pip install -r requirements.txt
```

### Check if brownie is installed
```bash
brownie --version
```

### Add chainstack rpc for polygon
```bash
brownie networks add Polygon "polygon-main-chainstack" host=https://<replace-with-your-credentials> chainid=137 name="Mainnet (Chainstack)" explorer=https://api.polygonscan.com/api
```

### Check if rpc was added

```bash
brownie console --network polygon-main-chainstack
```

### How to run the

```bash
./qi.sh VAULT ID
```
where 
VAULT = cwm for camWMATIC, cwe for camWETH
ID = vault ID

eg. To run the bot on the camWMATIC vault with id 1337

```bash
./qi.sh cwm 1337
```