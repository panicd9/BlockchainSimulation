import json

from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

from block import Block


class Node:

    def __init__(self, block: Block):
        self.block = block

    @staticmethod
    def verify_signature(public_key: bytes, signature: bytes, transaction_data: bytes):
        public_key = ECC.import_key(public_key)
        transaction_hash = SHA256.new(transaction_data)
        print("PUBLIC TEST 1: " + str(public_key))
        print("HASH TEST 1: " + str(transaction_hash.hexdigest()))
        print("KLJUC 1: " + str(public_key))
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
