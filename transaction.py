import binascii
import json
from datetime import datetime

from Crypto.Hash import keccak, SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from cryptography import calculate_hash
from wallet import Wallet


def transaction_object_from_json(transaction_json):
    transaction = Transaction(None, None, None)
    print(transaction_json['sender_public_key'])
    transaction.sender = ECC.import_key(transaction_json['sender_public_key'])
    transaction.receiver_address = transaction_json['receiver'][2:]
    transaction.amount = transaction_json['amount']
    transaction.timestamp = datetime.strptime(transaction_json['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
    transaction.signature = binascii.unhexlify(transaction_json['signature'])

    return transaction


class Transaction:
    def __init__(self, sender: Wallet, receiver_address: bytes, amount: int):

        self.sender = sender
        if self.sender != "Coinbase":
            # redni broj transakcije svakog Wallet-a
            self.sender_transaction_id = self.sender.transaction_id + 1
            # povecamo taj broj za 1
            self.sender.transaction_id = self.sender.transaction_id + 1
        self.receiver_address = receiver_address
        self.amount = amount
        self.timestamp = datetime.now()
        self.signature = ""
        self.sign()

    def generate_transaction_data(self) -> dict:
        if self.sender != "Coinbase":
            sender = '0x' + self.sender.address
        else:
            sender = "Coinbase"
        return {
            "sender": "0x" + sender,
            "receiver": '0x' + str(self.receiver_address),
            "amount": str(self.amount),
            "timestamp": str(self.timestamp)
        }

    def sign(self) -> str:
        if self.sender == "Coinbase":
            return
        transaction_data = bytearray(json.dumps(self.generate_transaction_data(), indent=4).encode('utf-8'))
        _hash = SHA256.new(transaction_data)
        signer = DSS.new(self.sender.private_key, 'fips-186-3')
        self.signature = signer.sign(_hash)


    def to_json(self):
        # public_key_ascii = ECC.import_key(self.sender.public_key).export_key(format='PEM')
        if self.signature != "":
            signature = binascii.hexlify(self.signature).decode("utf-8")
        else:
            signature = ""
        return {
            "sender_public_key": self.sender.public_key,
            "sender": '0x' + self.sender.address,
            "receiver": '0x' + self.receiver_address,
            "amount": self.amount,
            "timestamp": str(self.timestamp),
            "signature": signature
        }

    def __str__(self):

        if self.sender != "Coinbase":
            sender = '0x' + self.sender.address
            sender_transaction_id = self.sender_transaction_id
            sender_public_key = self.sender.public_key
        else:
            sender = "Coinbase"
            sender_transaction_id = -1
            sender_public_key = "Coinbase"

        if self.signature != "":
            signature = binascii.hexlify(self.signature).decode("utf-8")
        else:
            signature = ""

        return str({
            "sender_transaction_id": sender_transaction_id,
            "sender_public_key": sender_public_key,
            "sender": sender,
            "receiver": '0x' + self.receiver_address,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "signature": signature
        })

    def __repr__(self):
        return '\n' + str(self)
