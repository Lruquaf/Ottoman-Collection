from brownie import OttomanCollection
from .helpful_scripts import get_account, get_contract

account_names = {
    0: "from_key",
    1: "from_key_test_1",
    2: "from_key_test_2",
    3: "from_key_test_3",
    4: "from_key_test_4",
    5: "from_key_test_5",
}

token_uris = {
    "osman_i": "ipfs://QmWVE3ccNqthcioDxrWJSnCYxiLNmqkTE6HnLDNHPb7T4a?filename=1-osman_i.json",
    "orhan": "ipfs://QmaGUTZ7oM732y2c9Zy5mEcNnbwuTSKiKdyr52LCUqwfod?filename=2-orhan.json",
    "murad_i": "ipfs://QmcCrSD9q21bv7iRxJcE498Lmdc4aR7DVr9ac6qQKcQBHQ?filename=3-murad_i.json",
    "bayeid_i": "ipfs://QmbFfJ9URz8pakNSafB7237mQmSccpfw8A7GwmHbcyZd9k?filename=4-bayezid_i.json",
    "mehmed_i": "ipfs://QmYdG2eBp2TPTKtgpgDBioHf194y7xKDKLSkEVwC3GaSdp?filename=5-mehmed_i.json",
    "murad_ii": "ipfs://Qmanb8kwDbWKTi8WXFTZEURUdRMBrY6sGstWQjwF2Dqcnf?filename=6-murad_ii.json",
}


def create_collectible():
    account = get_account()
    nft_contract = OttomanCollection[-1]
    token_uri, token_id = get_token_uri(nft_contract)
    create_nft_tx = nft_contract.createCollectible(token_uri, {"from": account})
    create_nft_tx.wait(1)
    print(
        "The collectible with id {} was created by {} at {} successfully!".format(
            token_id, account, nft_contract.address
        )
    )


def get_token_uri(nft_contract):
    token_id = nft_contract.tokenCounter()
    sultan = nft_contract.sultans(token_id)
    token_uri = token_uris[str(sultan)]
    return token_uri, token_id


def purchase_collectible(name, token_id):
    account = get_account(name=name)
    nft_contract = OttomanCollection[-1]
    token_contract = get_contract("ottoman_token")
    approve_tx = token_contract.approve(
        nft_contract.address, nft_contract.costInOTT(), {"from": account}
    )
    approve_tx.wait(1)
    purchase_nft_tx = nft_contract.purchaseCollectible(token_id, {"from": account})
    purchase_nft_tx.wait(1)
    print(
        "The collectible with id {} was purchased by {} from {} successfully!".format(
            token_id, account, nft_contract.address
        )
    )


def withdraw_tokens():
    account = get_account()
    nft_contract = OttomanCollection[-1]
    withdraw_tx = nft_contract.withdrawTokens({"from": account})
    withdraw_tx.wait(1)
    print("The tokens were withdrew by {}".format(account))


def main():
    i = 0
    while i != 6:
        create_collectible()
        i += 1
    for j in range(1, 6):
        purchase_collectible(account_names[j], j)
    withdraw_tokens()
