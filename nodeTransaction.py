import binascii
import json
from datetime import datetime

from Crypto.Hash import keccak, SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from cryptography import calculate_hash
from transaction import Transaction
from utils import address_from_public_key


def nodeTransaction_object_from_json(transaction_json):
    transaction = NodeTransaction(transaction_json['sender_public_key'])
    transaction.sender = ECC.import_key(transaction_json['sender_public_key'])
    transaction.receiver_address = transaction_json['receiver']
    transaction.amount = transaction_json['amount']
    transaction.timestamp = transaction_json['timestamp']
    transaction.signature = binascii.unhexlify(transaction_json['signature'])

    return transaction

## SENDER IS PUBLIC KEY !!!
class NodeTransaction:
    def __init__(self, sender_public_key):
        self.sender = sender_public_key
        self.sender_address = address_from_public_key(ECC.import_key(self.sender))
        self.receiver_address = ""
        self.amount = ""
        self.timestamp = ""
        self.signature = ""

    def generate_transaction_data(self) -> dict:
        return {
            "sender": '0x' + self.sender_address,
            "receiver": '0x' + str(self.receiver_address),
            "amount": str(self.amount),
            "timestamp": str(self.timestamp)
        }

    def to_json(self):
        # public_key_ascii = ECC.import_key(self.sender.public_key).export_key(format='PEM')
        # print(self.sender)
        return {
            "sender_public_key": self.sender.export_key(format='PEM'),
            "sender": '0x' + self.sender_address,
            "receiver": '0x' + self.receiver_address,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "signature": binascii.hexlify(self.signature).decode("utf-8")
        }

    def __str__(self):
        # public_key_ascii = ECC.import_key(self.sender.public_key).export_key(format='PEM')
        return str({
            "sender_public_key": self.sender.export_key(format='PEM'),
            "sender": '0x' + self.sender_address,
            "receiver": '0x' + self.receiver_address,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "signature": binascii.hexlify(self.signature).decode("utf-8")
        })

    def __repr__(self):
        return '\n' + str(self)
