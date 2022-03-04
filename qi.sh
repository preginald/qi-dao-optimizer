#!/usr/bin/env bash

if [[ -z "${p1}" ]]; then
    echo -n "Enter p1: "
    read -s p1
    export p1=$p1
    echo ""
fi

if [[ -z "${POLYGONSCAN_TOKEN}" ]]; then
    echo -n "Enter Polygonscan API token: "
    read -s api_token 
    export POLYGONSCAN_TOKEN=$api_token
    echo ""
fi

if [ -z "$1" ]; then
    echo -n "Enter the Brownie Account ID: "
    read acc_id
else
    acc_id=$1
fi

if [[ "$2" =~ ^(cwb|cwe|cwm)$ ]]; then
    vault_asset=$2
else
    echo "Select which vault"
    echo -n "cwm = camWMATIC, cwe = camWETH, cwb = camWBTC: "
    read vault_asset
fi

if [ -z "$3" ]; then
    echo -n "Enter the $function vault ID: "
    read vault_id
else
    vault_id=$3
fi

if [ -z "$4" ]; then
    echo -n "Enter the network ID: "
    read network_id
else
    network_id=$4
fi

declare -A functions=( ["cwm"]="camWMATIC" ["cwe"]="camWETH")

function=${functions[$vault_asset]}

while :
do
    counter=5
    echo
    echo Running $function on $network_id
    echo
    brownie run scripts/qi_dao.py $function $acc_id $vault_id --network $network_id
    echo 
    while [ $counter -gt -1 ]
    do
        echo Waiting $counter seconds
        counter=$(( $counter - 1 ))
        sleep 1
    done
done
