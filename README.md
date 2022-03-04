## Qi Dao vault optimizer

## Prequisites

* python 3.9
* eth-brownie 1.17.2
* python3-env
* python3-dev 


## Steps to install

### Install Python virtual environent

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

### Check if Brownie is installed
```bash
brownie --version
```

### Add Alchemy RPC for Polygon
```bash
brownie networks add Polygon "polygon-main-alchemy" host=https://<replace-with-your-credentials> chainid=137 name="Mainnet (Alchemy)" explorer=https://api.polygonscan.com/api
```

### Add Chainstack RPC for Polygon
```bash
brownie networks add Polygon "polygon-main-chainstack" host=https://<replace-with-your-credentials> chainid=137 name="Mainnet (Chainstack)" explorer=https://api.polygonscan.com/api
```

### Check if RPC was added

```bash
brownie console --network polygon-main-alchemy
```

```bash
brownie console --network polygon-main-chainstack
```

### Add Brownie Account credentials

```bash
brownie accounts new <account_id>
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