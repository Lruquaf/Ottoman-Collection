import json
from pathlib import Path
from brownie import OttomanCollection, network
from metadata import metadata_sample
import requests


def write_metadata():
    nft_contract = OttomanCollection[-1]
    for num in range(nft_contract.numberOfSultans()):
        metadata = metadata_sample.metadata_template
        sultan = nft_contract.sultans(num)
        metadata_file_name = (
            "./metadata/{}/".format(network.show_active())
            + str(num + 1)
            + "-"
            + sultan
            + ".json"
        )
        if Path(metadata_file_name).exists():
            print(
                "{} already found, delete it to overwrite!".format(metadata_file_name)
            )
        else:
            print("Creating metadata file: " + metadata_file_name)
            metadata["name"]["name"] = str(input("name: "))
            metadata["name"]["title"] = str(input("title: "))
            metadata["name"]["titled_name"] = str(input("titled name: "))
            metadata["age"]["born"] = str(input("born: "))
            metadata["age"]["died"] = str(input("died: "))
            metadata["age"]["age"] = str(input("age: "))
            metadata["reign"]["reign_from"] = str(input("reign from: "))
            metadata["reign"]["reign_to"] = str(input("reign to: "))
            metadata["reign"]["reign"] = str(input("reign: "))
            metadata["reign"]["predecessor"] = str(input("predecessor: "))
            metadata["reign"]["successor"] = str(input("successor: "))
            metadata["family"]["father"] = str(input("father: "))
            metadata["family"]["mother"] = str(input("mother: "))
            metadata["dynasty"] = str(input("dynasty: "))
            metadata["image"] = get_image_uri(num)
            with open(metadata_file_name, "w") as file:
                json.dump(metadata, file)
            upload_to_ipfs(metadata_file_name)


def get_image_uri(num):
    nft_contract = OttomanCollection[-1]
    image_path = "./sultans/" + nft_contract.sultans(num) + ".jpg"
    image_uri = upload_to_ipfs(image_path)
    return image_uri


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = "ipfs://{}?filename={}".format(ipfs_hash, filename)
        print(image_uri)
    return image_uri


def main():
    write_metadata()
