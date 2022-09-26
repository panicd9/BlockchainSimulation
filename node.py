import json

import requests as requests
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

from otherNode import OtherNode
from transaction import Transaction


class Node:

    def __init__(self, block, ip="127.0.0.1", port=8080):
        self.base_url = f"http://{ip}:{port}/"
        self.block = block
        self.node_list = [OtherNode("127.0.0.1", 8082), OtherNode("127.0.0.1", 8083)]

    @staticmethod
    def verify_signature(public_key: bytes, signature: bytes, transaction: Transaction):
        public_key = ECC.import_key(public_key)
        transaction_data = bytearray(json.dumps(transaction.generate_transaction_data(), indent=4).encode('utf-8'))
        transaction_hash = SHA256.new(transaction_data)
        # print("PUBLIC TEST 1: " + str(public_key))
        # print("HASH TEST 1: " + str(transaction_hash.hexdigest()))
        # print("KLJUC 1: " + str(public_key))
        return DSS.new(public_key, 'fips-186-3').verify(transaction_hash, signature)

    def validate_funds(self, sender_address: bytes, amount: int) -> bool:
        sender_balance = 0
        current_block = self.block
        while current_block:
            for transaction in current_block.transactions:
                if transaction["sender"] == sender_address:
                    sender_balance = sender_balance - transaction["amount"]
                if transaction["receiver"] == sender_address:
                    sender_balance = sender_balance + transaction["amount"]
            current_block = current_block.previous_block
        if amount <= sender_balance:
            return True
        else:
            return False

    def proof_of_work_test(self):
        current_block = self.block
        blockchain_from_start = []
        while current_block:
            blockchain_from_start.append(current_block)
            current_block = current_block.previous_block
        blockchain_from_start = list(reversed(blockchain_from_start))

        for block in blockchain_from_start:
            block.proof_of_work_block()

    def send_transaction_to_other_node(self, transaction: dict, url: str) -> requests.Response:
        url = f"{self.base_url}send_transaction"
        req_return = requests.post(url, json=transaction)
        req_return.raise_for_status()
        return req_return

    def broadcast(self, transaction: dict):
        for otherNode in self.node_list:
            try:
                self.send_transaction_to_other_node(transaction, otherNode.base_url)
            except requests.ConnectionError:
                pass
