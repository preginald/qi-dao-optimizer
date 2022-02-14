#!/usr/bin/env bash

echo "Select which vault"
echo -n "cwm = camWMATIC, cwe = camWETH, cwb = camWBTC: "
read vault_asset

brownie run scripts/qi_dao_unit.py $vault_asset polygon-main-chainstack