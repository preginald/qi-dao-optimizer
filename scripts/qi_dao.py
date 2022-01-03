#!/usr/bin/python3
from brownie import (
    PriceFeedConsumer,
    accounts,
    config,
    interface,
    network,
    Contract,
    Wei,
)
import time, os

camWMATIC_CONTRACT = "0x88d84a85A87ED12B8f098e8953B322fF789fCD1a"
camWBTC_CONTRACT = "0x7dda5e1a389e0c1892caf55940f5fce6588a9ae0"
camWETH_CONTRACT = "0x11a33631a5b5349af3f165d2b7901a4d67e561ad"
MATIC_CONTRACT_ADDRESS = "0xAB594600376Ec9fD91F8e885dADF0CE036862dE0"
BTC_CONTRACT_ADDRESS = "0xc907E116054Ad103354f2D350FD2514433D57F6f"
ETH_CONTRACT_ADDRESS = "0xF9680D99D6C9589e2a93a78A04A279e509205945"

# ACC_ID = "test1"

ACC_ID = "alpha"


def get_account(_filename):
    account = accounts.load(_filename, os.environ["p1"])
    account_balance = account.balance() / 10 ** 18
    print("Account loaded")
    print("Balance:", account_balance)
    return account


def get_token_price(contract_address):
    contract = interface.ChainlinkPriceFeed(contract_address)
    # contract = Contract.from_explorer(contract_address)
    decimals = 10 ** contract.decimals()
    price = contract.latestAnswer() / decimals
    # print(f"Price: ${price}")
    return price


class Vault:
    def __init__(self, vault, vault_id):
        self.vault = vault
        self.vault_id = vault_id

        self.debt = self.get_debt()

        if vault.name() == "camWMATIC MAI Vault":
            self.max_debt_ratio = 180
            self.min_debt_ratio = 190
            self.precision = 10 ** 18
            contract_address = MATIC_CONTRACT_ADDRESS

        if vault.name() == "camWETH MAI Vault":
            self.max_debt_ratio = 180
            self.min_debt_ratio = 190
            self.precision = 10 ** 18
            contract_address = ETH_CONTRACT_ADDRESS

        if vault.name() == "camWBTC MAI Vault":
            self.max_debt_ratio = 155
            self.min_debt_ratio = 165
            self.precision = 10 ** 8
            contract_address = BTC_CONTRACT_ADDRESS

        self.collateral_price = get_token_price(contract_address)
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
        amount = Wei(f"{self.borrow_amount} ether")
        print(f"You are about to borrow {amount}")
        tx = self.vault.borrowToken(self.vault_id, amount, {"from": acc})
        tx.wait(5)
        return tx

    def repay(self):
        acc = get_account(ACC_ID)
        amount = self.max_borrow - self.debt
        amount = Wei(f"{abs(amount)} ether")
        print(f"You are about to repay {amount}")
        tx = self.vault.payBackToken(self.vault_id, amount, {"from": acc})
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


def camWMATIC():
    vault_contract = interface.MaiVault(camWMATIC_CONTRACT)
    # vault_contract = Contract.from_explorer(camWMATIC_CONTRACT)
    vault_id = 2032  # alpha
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
    # vault_contract = Contract.from_explorer(camWMATIC_CONTRACT)
    vault_id = 1227  # alpha
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
    # vault_contract = Contract.from_explorer(camWBTC_CONTRACT)
    vault_id = 506
    vault = Vault(vault_contract, vault_id)

    if vault.collateral_to_debt_ratio < vault.max_debt_ratio:  # 160
        tx = vault.repay()

    if vault.collateral_to_debt_ratio > vault.min_debt_ratio:  # 180
        if vault.mai_reserves < 10:
            print("Not enough MAI to borrow.")
        else:
            tx = vault.borrow()


def main():
    while True:
        camWMATIC()
        print("")
        time.sleep(5)
        camWETH()
        print("")
        time.sleep(5)
        camWBTC()
        print("")
        time.sleep(5)
