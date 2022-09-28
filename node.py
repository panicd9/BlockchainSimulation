import json

import requests as requests
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

import nodeTransaction
from otherNode import OtherNode
from transaction import Transaction


class Node:

    def __init__(self, block, name, miner_address):
        self.name = name
        self.block = block
        self.miner_address = miner_address

    # @staticmethod
    # def verify_signature(public_key: bytes, signature: bytes, transaction: Transaction):
    #     public_key = ECC.import_key(public_key)
    #     transaction_data = bytearray(json.dumps(transaction.generate_transaction_data(), indent=4).encode('utf-8'))
    #     transaction_hash = SHA256.new(transaction_data)
    #     # print("PUBLIC TEST 1: " + str(public_key))
    #     # print("HASH TEST 1: " + str(transaction_hash.hexdigest()))
    #     # print("KLJUC 1: " + str(public_key))
    #     return DSS.new(public_key, 'fips-186-3').verify(transaction_hash, signature)

    def proof_of_work_test(self):
        current_block = self.block
        blockchain_from_start = []
        while current_block:
            blockchain_from_start.append(current_block)
            current_block = current_block.previous_block
        blockchain_from_start = list(reversed(blockchain_from_start))

        for block in blockchain_from_start:
            block.proof_of_work_block()

    def start_pow(self, blocks):
        for i, block in enumerate(blocks):
            block.proof_of_work_block(node_name=self.name, miner_address=self.miner_address)

    def send_transaction_to_other_node(self, transaction: nodeTransaction, url: str) -> requests.Response:
        url = f"{self.base_url}send_transaction"
        req_return = requests.post(url, json=transaction.to_json())
        req_return.raise_for_status()
        return req_return

    def broadcast(self, transaction: dict):
        for otherNode in self.node_list:
            try:
                self.send_transaction_to_other_node(transaction, otherNode.base_url)
            except requests.ConnectionError:
                pass
