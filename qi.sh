#!/usr/bin/env bash

if [[ "$1" =~ ^(cwb|cwe|cwm)$ ]]; then
    vault_asset=$1
else
    echo "Select which vault"
    echo -n "cwm = camWMATIC, cwe = camWETH, cwb = camWBTC: "
    read vault_asset
fi

if [ -z "$2" ]; then
    echo "Enter the $function vault ID"
    read vault_id
else
    vault_id=$2
fi

declare -A functions=( ["cwm"]="camWMATIC" ["cwe"]="camWETH")

function=${functions[$vault_asset]}

while :
do
    brownie run scripts/qi_dao_unit.py $function $vault_id --network polygon-main-chainstack
    echo 
    sleep 5s
done