import requests, json


def main(vault_type, vault_id):
    print(vault_type)
    print(vault_id)
    chain_id = "matic"
    camWBTC = "0xba6273a78a23169e01317bd0f6338547f869e8df"
    camWMATIC = "0x7068ea5255cb05931efa8026bd04b18f3deb8b0b"
    camWETH = "0x0470cd31c8fcc42671465880ba81d631f0b76c1d"
    # price = get_price(chain_id, camWMATIC)
    # price = content["price"]
    # qty = 0.02418717
    # total = price * qty
    # print(price, qty, total)


def get_price(chain_id, id):
    url = "https://openapi.debank.com/v1/token"
    params = {"chain_id": chain_id, "id": id}
    response = requests.get(url, params)
    return json.loads(response.content)["price"]
