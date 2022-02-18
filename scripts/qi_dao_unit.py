#!/usr/bin/python3
from brownie import (
    accounts,
    config,
    interface,
    network,
    Contract,
    Wei,
)
import requests, json, time, os
from web3 import Web3

camWMATIC_CONTRACT = config["networks"][network.show_active()]["tokens"]["camWMATIC"]
camWBTC_CONTRACT = config["networks"][network.show_active()]["tokens"]["camWBTC"]
camWETH_CONTRACT = config["networks"][network.show_active()]["tokens"]["camWETH"]
MATIC_CONTRACT_ADDRESS = config["networks"][network.show_active()][
    "matic_usd_price_feed"
]
BTC_CONTRACT_ADDRESS = config["networks"][network.show_active()]["btc_usd_price_feed"]
ETH_CONTRACT_ADDRESS = config["networks"][network.show_active()]["eth_usd_price_feed"]

ACC_ID = config["wallets"]["from_id"]


class Vault:
    def __init__(self, vault, vault_id):
        self.vault = vault
        self.vault_id = vault_id

        self.debt = self.get_debt()

        self.max_debt_ratio = config["networks"][network.show_active()][vault.name()][
            "max_debt_ratio"
        ]
        self.min_debt_ratio = config["networks"][network.show_active()][vault.name()][
            "min_debt_ratio"
        ]
        self.precision = (
            10 ** config["networks"][network.show_active()][vault.name()]["precision"]
        )
        contract_address = config["networks"][network.show_active()][vault.name()][
            "price_feed"
        ]

        self.collateral_price = get_price_chainlink(contract_address)
        self.collateral = vault.vaultCollateral(vault_id) / self.precision
        self.collateral_value = self.collateral * self.collateral_price

        self.collateral_to_debt_ratio = (self.collateral_value / self.debt) * 100
        self.max_borrow = self.collateral_value / (self.max_debt_ratio / 100)
        self.min_borrow = self.collateral_value / (self.min_debt_ratio / 100)

        self.borrow_amount = self.min_borrow - self.debt
        self.borrow_amount_wei = Wei(f"{self.borrow_amount} ether")

        self.mai_reserves = self.get_debt_ceiling()

        self.print_values()

    def print_values(self):
        print(f"{self.vault.name()}: ${self.collateral_price}")
        print(f"Collateral (USD): ${round(self.collateral_value,3)}")
        print(f"Collateral: {round(self.collateral,3)} in {self.vault.name()}")

        print(f"Debt ceiling: {round(self.mai_reserves,3)} MAI")
        print(f"Debt: {self.debt} MAI")

        print(f"Collateral to debt ratio: {round(self.collateral_to_debt_ratio, 0)}")
        print(f"Max debt ratio: {self.max_debt_ratio}")
        print(f"Min debt ratio: {self.min_debt_ratio}")

    def borrow(self):
        acc = get_account(ACC_ID)

        if self.mai_reserves < self.borrow_amount:
            amount = self.mai_reserves - 1
        else:
            amount = self.borrow_amount

        if amount < 1:
            print(f"You need to borrow more than 1 miMATIC {amount}!")
            return
        else:
            amount_wei = Wei(f"{amount} ether")
            print(f"You are about to borrow {amount} ({amount_wei})")
            tx = self.vault.borrowToken(self.vault_id, amount_wei, {"from": acc})
            tx.wait(5)
            return tx

    def repay(self):
        acc = get_account(ACC_ID)
        amount = self.debt - self.max_borrow
        if amount > 10:
            amount_wei = Web3.toWei(amount, "ether")
            print(f"You are about to repay {amount} ({amount_wei})")
            tx = self.vault.payBackToken(self.vault_id, amount_wei, {"from": acc})
            tx.wait(5)
        else:
            print(f"Skipping repay {amount} because amount is less than 10.")
            tx = False
        return tx

    def get_debt_ceiling(self):
        debt_ceiling = self.vault.getDebtCeiling() / 10 ** 18
        # print(f"Debt ceiling: {round(debt_ceiling,3)} MAI")
        return debt_ceiling

    def get_debt(self):
        debt = self.vault.vaultDebt(self.vault_id) / 10 ** 18
        # print(f"Debt: {debt} MAI")
        return debt


def get_account(_filename):
    account = accounts.load(_filename, os.environ["p1"])
    account_balance = account.balance() / 10 ** 18
    print("Account loaded")
    print("Balance:", account_balance)
    return account


def get_price_chainlink(contract_address):
    contract = interface.ChainlinkPriceFeed(contract_address)
    # contract = Contract.from_explorer(contract_address)
    decimals = 10 ** contract.decimals()
    price = contract.latestAnswer() / decimals
    # print(f"Price: ${price}")
    return price


def get_price_debank(chain_id, id):
    url = "https://openapi.debank.com/v1/token"
    params = {"chain_id": chain_id, "id": id}
    response = requests.get(url, params)
    return json.loads(response.content)["price"]


def camWMATIC(vault_id):
    vault_contract = interface.MaiVault(camWMATIC_CONTRACT)
    # vault_id = config["networks"][network.show_active()]["camWMATIC MAI Vault"]["id"]
    vault = Vault(vault_contract, vault_id)

    if vault.collateral_to_debt_ratio < vault.max_debt_ratio:  # 160
        tx = vault.repay()

    if vault.collateral_to_debt_ratio > vault.min_debt_ratio:  # 180
        if vault.mai_reserves < 10:
            print("Not enough MAI to borrow.")
        else:
            tx = vault.borrow()


def camWETH(vault_id):
    vault_contract = interface.MaiVault(camWETH_CONTRACT)
    # vault_id = config["networks"][network.show_active()]["camWETH MAI Vault"]["id"]
    vault = Vault(vault_contract, vault_id)

    if vault.collateral_to_debt_ratio < vault.max_debt_ratio:  # 160
        tx = vault.repay()

    if vault.collateral_to_debt_ratio > vault.min_debt_ratio:  # 180
        if vault.mai_reserves < 10:
            print("Not enough MAI to borrow.")
        else:
            tx = vault.borrow()


def camWBTC(vault_id):
    vault_contract = interface.MaiVault(camWBTC_CONTRACT)
    # vault_id = config["networks"][network.show_active()]["camWBTC MAI Vault"]["id"]
    vault = Vault(vault_contract, vault_id)

    if vault.collateral_to_debt_ratio < vault.max_debt_ratio:  # 160
        tx = vault.repay()

    if vault.collateral_to_debt_ratio > vault.min_debt_ratio:  # 180
        if vault.mai_reserves < 10:
            print("Not enough MAI to borrow.")
        else:
            tx = vault.borrow()


def main():
    print("Asset codes: cwm = camWMATIC, cwe = camWETH, cwb = camWBTC")
    vault_asset = input("Enter asset: ")
    while True:
        if vault_asset == "cwm":
            camWMATIC()
        if vault_asset == "cwe":
            camWETH()
        if vault_asset == "cwb":
            camWBTC()
        print("")
        time.sleep(5)
