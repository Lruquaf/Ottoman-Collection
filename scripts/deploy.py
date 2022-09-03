from brownie import OttomanCollection, config, network
from .helpful_scripts import get_account, get_contract


def deploy_contract():
    account = get_account()
    ottoman_collection = OttomanCollection.deploy(
        get_contract("ottoman_token").address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print(f"The contract has deployed at {ottoman_collection.address} successfully!")
    return ottoman_collection


def main():
    deploy_contract()
