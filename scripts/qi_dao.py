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


def get_network(network_id):
    network_array = network_id.split("-")
    return network_array[0] + "-" + network_array[1]


NETWORK_ID = get_network(network.show_active())
MAI_CONTRACT = config["networks"][NETWORK_ID]["tokens"]["mai"]


class Vault:
    def __init__(self, vault, acc_id, vault_id):
        self.vault = vault
        self.acc_id = acc_id
        self.vault_id = vault_id

        self.acc = get_account(self.acc_id)

        self.debt = self.get_debt()

        self.max_debt_ratio = config["networks"][NETWORK_ID][vault.name().strip()][
            "max_debt_ratio"
        ]
        self.min_debt_ratio = config["networks"][NETWORK_ID][vault.name().strip()][
            "min_debt_ratio"
        ]
        self.precision = (
            10 ** config["networks"][NETWORK_ID][vault.name().strip()]["precision"]
        )

        self.collateral_price = self.get_collateral_price()
        self.collateral = vault.vaultCollateral(vault_id) / self.precision
        self.collateral_value = self.collateral * self.collateral_price

        self.max_borrow = self.collateral_value / (self.max_debt_ratio / 100)
        self.min_borrow = self.collateral_value / (self.min_debt_ratio / 100)

        if self.debt > 0:
            self.collateral_to_debt_ratio = (self.collateral_value / self.debt) * 100
            self.borrow_amount = self.min_borrow - self.debt
        else:
            self.collateral_to_debt_ratio = self.min_debt_ratio * 1.1
            self.borrow_amount = self.min_borrow

        self.borrow_amount_wei = Wei(f"{self.borrow_amount} ether")

        self.mai_reserves = self.get_debt_ceiling()

        self.print_values()

    def print_values(self):
        print(f"{self.vault.name()}: ${round(self.collateral_price, 3)}")

        print(f"Collateral: {round(self.collateral,3)} in {self.vault.name()}")
        print(f"Collateral (USD): ${round(self.collateral_value,2)}")

        print(f"Debt ceiling: {round(self.mai_reserves,3)} MAI")
        print(f"Debt: {round(self.debt, 3)} MAI")
        print(f"Collateral to debt ratio: {round(self.collateral_to_debt_ratio, 2)}%")

        print(f"Max debt ratio: {self.max_debt_ratio}%")
        print(f"Min debt ratio: {self.min_debt_ratio}%")

    def borrow(self):
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
            tx = self.vault.borrowToken(self.vault_id, amount_wei, {"from": self.acc})
            tx.wait(5)
            return tx

    def repay(self):
        amount = self.debt - self.max_borrow
        if amount > self.debt / 100:
            amount_wei = Web3.toWei(amount, "ether")
            print(f"You are about to repay {amount} ({amount_wei})")
            tx = self.vault.payBackToken(self.vault_id, amount_wei, {"from": self.acc})
            tx.wait(5)
        else:
            print(f"Skipping repay {amount} because amount is less than 10.")
            tx = False
        return tx

    def get_debt_ceiling(self):
        debt_ceiling = self.vault.getDebtCeiling() / 10 ** 18
        return debt_ceiling

    def get_debt(self):
        debt = self.vault.vaultDebt(self.vault_id) / 10 ** 18
        return debt

    def get_collateral_price(self):
        return self.vault.getEthPriceSource() / 10 ** 8


def get_account(_filename):
    native = config["networks"][NETWORK_ID]["native"]
    account = accounts.load(_filename, os.environ["p1"])
    account_balance = account.balance() / 10 ** 18
    print("Account loaded")
    print(native, "Balance:", round(account_balance, 3))
    print("MAI Balance:", round(get_token_balance(MAI_CONTRACT, account.address), 3))
    print("")
    return account


def get_token_balance(contract_address, account_address):
    url = config["networks"][NETWORK_ID]["url"]
    explorer_token = config["networks"][NETWORK_ID]["env_name"]
    params = {
        "module": "account",
        "action": "tokenbalance",
        "contractaddress": contract_address,
        "address": account_address,
        "tag": "latest",
        "apikey": os.environ[explorer_token],
    }

    response = requests.get(url, params)
    return int(json.loads(response.content)["result"]) / 10 ** 18


def get_price_chainlink(contract_address):
    contract = interface.ChainlinkPriceFeed(contract_address)
    decimals = 10 ** contract.decimals()
    price = contract.latestAnswer() / decimals
    return price


def main(vault_contract, acc_id, vault_id):
    vault_contract_address = config["networks"][NETWORK_ID]["tokens"][vault_contract]
    vault_contract = interface.MaiVault(vault_contract_address)
    vault = Vault(vault_contract, acc_id, vault_id)

    if vault.collateral_to_debt_ratio < vault.max_debt_ratio:  # 150
        tx = vault.repay()

    if vault.collateral_to_debt_ratio > vault.min_debt_ratio:  # 165
        if vault.mai_reserves < 10:
            print("Not enough MAI to borrow.")
        else:
            tx = vault.borrow()
