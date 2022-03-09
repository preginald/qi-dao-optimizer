#!/usr/bin/env bash

LCYAN='\033[1;36m'
LGREEN='\033[1;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color


sleep 10

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

if [[ "$2" =~ ^(cwm|cxd)$ ]]; then
    vault_asset=$2
else
    echo "Select which vault"
    echo -n "cwm = camWMATIC, cxd = cxDOGE: "
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

declare -A functions=( ["cwm"]="camWMATIC" ["cxd"]="cxDMVT" )

function=${functions[$vault_asset]}

while :
do
    counter=5
    echo
    printf "Running ${LCYAN}${function}${NC} vault ${YELLOW}#${vault_id}${NC} on ${LGREEN}${network_id}${NC}\n"
    echo
    brownie run scripts/qi_dao.py main $function $acc_id $vault_id --network $network_id
    echo 
    while [ $counter -gt -1 ]
    do
        echo Waiting $counter seconds
        counter=$(( $counter - 1 ))
        sleep 1
    done
done
