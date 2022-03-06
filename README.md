## Qi Dao vault optimizer

The main reason I created this bot is so that I could sleep at night knowing that my vaults are earning the maximum Qi rewards.

## How it works ##

The bot borrows or pays back the loan on your vault automatically based on the underlying collateral price.

The cycle time for the bot is ~ 20 seconds. This means that every 20 seconds the bot performs the following tasks:

* check the collateral token price
* check if the collateral to debt ratio is within the defined "safe" limit.
* eg. on the camWMATIC vault, if CDR is < 160% then it will repay MAI to bring it back to over 160% CDR. 
* Conversely, if CDR is > 170% then it will borrow MAI (if debt ceiling > 10 MAI). 

The bot loop execution is performed by a bash shell script which calls the brownie script instead of running the loop in the python script for improved reliability.

![screenshot of the camWMATIC and cxDOGE bots in action](https://ibb.co/Dpcn5jv)


## Prequisites

* Ubuntu (or a Linux distro with bash)
* python 3.9
* eth-brownie 1.17.2
* python3-env
* python3-dev 


## IMPORTANT ##
Test the bot on a small vault deposit initially until you get a good feel for the way the bot runs.

You must make sure that you have approved the borrow and payback actions for the vault you wish to run this bot on. Failure to do this will result in a ValueError error and the bot will fail. 


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