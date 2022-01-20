## Qi Dao vault optimizer

## Prequisites

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

