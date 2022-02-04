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

        self.collateral_price = get_price_debank("matic", contract_address)
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

        amount_wei = Wei(f"{amount} ether")
        print(f"You are about to borrow {amount} ({amount_wei})")
        tx = self.vault.borrowToken(self.vault_id, amount_wei, {"from": acc})
        tx.wait(5)
        return tx

    def repay(self):
        acc = get_account(ACC_ID)
        amount = self.max_borrow - self.debt
        amount_wei = Wei(f"{abs(amount)} ether")
        print(f"You are about to repay {amount} ({amount_wei})")
        tx = self.vault.payBackToken(self.vault_id, amount_wei, {"from": acc})
        tx.wait(5)
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


def get_price_debank(chain_id, id):
    url = "https://openapi.debank.com/v1/token"
    params = {"chain_id": chain_id, "id": id}
    response = requests.get(url, params)
    return json.loads(response.content)["price"]


def camWMATIC():
    vault_contract = interface.MaiVault(camWMATIC_CONTRACT)
    vault_id = config["networks"][network.show_active()]["camWMATIC MAI Vault"]["id"]
    vault = Vault(vault_contract, vault_id)

    if vault.collateral_to_debt_ratio < vault.max_debt_ratio:  # 160
        tx = vault.repay()

    if vault.collateral_to_debt_ratio > vault.min_debt_ratio:  # 180
        if vault.mai_reserves < 10:
            print("Not enough MAI to borrow.")
        else:
            tx = vault.borrow()


def camWETH():
    vault_contract = interface.MaiVault(camWETH_CONTRACT)
    vault_id = config["networks"][network.show_active()]["camWETH MAI Vault"]["id"]
    vault = Vault(vault_contract, vault_id)

    if vault.collateral_to_debt_ratio < vault.max_debt_ratio:  # 160
        tx = vault.repay()

    if vault.collateral_to_debt_ratio > vault.min_debt_ratio:  # 180
        if vault.mai_reserves < 10:
            print("Not enough MAI to borrow.")
        else:
            tx = vault.borrow()


def camWBTC():
    vault_contract = interface.MaiVault(camWBTC_CONTRACT)
    vault_id = config["networks"][network.show_active()]["camWBTC MAI Vault"]["id"]
    vault = Vault(vault_contract, vault_id)

    if vault.collateral_to_debt_ratio < vault.max_debt_ratio:  # 160
        tx = vault.repay()

    if vault.collateral_to_debt_ratio > vault.min_debt_ratio:  # 180
        if vault.mai_reserves < 10:
            print("Not enough MAI to borrow.")
        else:
            tx = vault.borrow()


def main():
    vault_asset = input("Enter asset: cwm = camWMATIC, cwe = camWETH, cwb = camWBTC")
    while True:
        if vault_asset == "cwm":
            camWMATIC()
        if vault_asset == "cwe":
            camWETH()
        if vault_asset == "cwb":
            camWBTC()
        print("")
        time.sleep(5)
