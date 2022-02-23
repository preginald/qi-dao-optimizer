#!/usr/bin/env bash

if [[ -z "${p1}" ]]; then
    echo -n "Enter p1: "
    read p1
    export p1=$p1
fi

if [[ "$1" =~ ^(cwb|cwe|cwm)$ ]]; then
    vault_asset=$1
else
    echo "Select which vault"
    echo -n "cwm = camWMATIC, cwe = camWETH, cwb = camWBTC: "
    read vault_asset
fi

if [ -z "$2" ]; then
    echo -n "Enter the $function vault ID: "
    read vault_id
else
    vault_id=$2
fi

if [ -z "$3" ]; then
    echo -n "Enter the network ID: "
    read network_id
else
    network_id=$3
fi

declare -A functions=( ["cwm"]="camWMATIC" ["cwe"]="camWETH")

function=${functions[$vault_asset]}

while :
do
    # brownie run scripts/qi_dao_unit.py $function $vault_id --network polygon-main-chainstack
    brownie run scripts/qi_dao_unit.py $function $vault_id --network $network_id
    echo 
    sleep 5s
done
