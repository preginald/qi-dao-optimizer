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

### Add Brownie account credentials

```bash
brownie accounts new <account_id>
```
### How to run the bot

```bash
./qi.sh <account_id> <vault> <id> <network>
```

where...

* **account_id** is the brownie account id specified when adding Brownie Account credentials
* **vault** is the collateral token code, cwm for camWMATIC, cwe for camWETH
* **id** is vault ID
* **network** is the brownie network id specified when adding a custom RPC

eg. To run the bot on the camWMATIC vault with id 1337 on the Alchemy Polygon RPC using the accound id of "alpha"

```bash
./qi.sh alpha cwm 1337 polygon-main-alchemy
```