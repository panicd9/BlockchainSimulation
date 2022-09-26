import binascii
import json
from datetime import datetime

from Crypto.Hash import keccak, SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from cryptography import calculate_hash


def transaction_object_from_json(transaction_json):
    transaction = Transaction(None, None, None)
    transaction.sender = ECC.import_key(transaction_json['sender_public_key'])
    transaction.receiver_address = transaction_json['receiver']
    transaction.amount = transaction_json['amount']
    transaction.timestamp = transaction_json['timestamp']
    transaction.signature = binascii.unhexlify(transaction_json['signature'])

    return transaction


class Transaction:
    def __init__(self, sender, receiver_address: bytes, amount: int):
        self.sender = sender
        self.receiver_address = receiver_address
        self.amount = amount
        self.timestamp = datetime.now()
        self.signature = ""

    def generate_transaction_data(self) -> dict:
        return {
            "sender": '0x' + str(self.sender.address),
            "receiver": '0x' + str(self.receiver_address),
            "amount": str(self.amount),
            "timestamp": str(self.timestamp)
        }

    def sign(self) -> str:
        # convert to bytes for hashing
        transaction_data = bytearray(json.dumps(self.generate_transaction_data(), indent=4).encode('utf-8'))
        # print("PODACI TEST 2: " + str(transaction_data))
        _hash = SHA256.new(transaction_data)
        # print("HASH TEST 2: " + str(_hash.hexdigest()))
        # print("javni: " + str(self.sender.public_key))
        # print("KLJUC 2: " + str(self.sender.private_key))
        signer = DSS.new(self.sender.private_key, 'fips-186-3')
        self.signature = signer.sign(_hash)
        print(self.signature)
        # self.signature = binascii.hexlify(self.signature).decode("utf-8")
        # print(self.signature)
        # print("POTPIS TEST 2: " + str(self.signature))
        # print("PRIVAT TEST 2: " + str(self.sender.private_key))

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
            "timestamp": self.timestamp,
            "signature": signature
        }

    def __str__(self):
        # public_key_ascii = ECC.import_key(self.sender.public_key).export_key(format='PEM')
        # print(self.signature)

        if self.signature != "":
            signature = binascii.hexlify(self.signature).decode("utf-8")
        else:
            signature = ""
        return str({
            "sender_public_key": self.sender,
            "sender": '0x' + self.sender.address,
            "receiver": '0x' + self.receiver_address,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "signature": signature
        })

    def __repr__(self):
        return '\n' + str(self)
