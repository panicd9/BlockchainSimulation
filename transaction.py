import binascii
import json
from datetime import datetime

from Crypto.Hash import keccak, SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from cryptography import calculate_hash


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
    def __init__(self, sender, receiver_address: bytes, amount: int):

        self.sender = sender
        if self.sender != "Coinbase":
            self.sender_transaction_id = self.sender.transaction_id + 1
            self.sender.transaction_id = self.sender.transaction_id + 1

        self.receiver_address = receiver_address
        self.amount = amount
        self.timestamp = datetime.now()
        self.signature = ""
        self.sign()
        print(self)

    def generate_transaction_data(self) -> dict:

        if self.sender != "Coinbase":
            sender = '0x' + self.sender.address
        else:
            sender = "Coinbase"

        # print(sender)
        # print(self.sender)
        return {
            "sender": "0x" + sender,
            "receiver": '0x' + str(self.receiver_address),
            "amount": str(self.amount),
            "timestamp": str(self.timestamp)
        }

    def sign(self) -> str:
        if type(self.sender) is str:
            return
        # convert to bytes for hashing
        transaction_data = bytearray(json.dumps(self.generate_transaction_data(), indent=4).encode('utf-8'))
        # print("PODACI TEST 2: " + str(transaction_data))
        # print(self.sender.public_key)
        # print(transaction_data)
        _hash = SHA256.new(transaction_data)
        # print("HASH TEST 2: " + str(_hash.hexdigest()))
        # print("javni: " + str(self.sender.public_key))
        # print("KLJUC 2: " + str(self.sender.private_key))
        signer = DSS.new(self.sender.private_key, 'fips-186-3')
        self.signature = signer.sign(_hash)
        # print(self.signature)
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
            "timestamp": str(self.timestamp),
            "signature": signature
        }

    def __str__(self):

        if self.sender != "Coinbase":
            sender = '0x' + self.sender.address,
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
