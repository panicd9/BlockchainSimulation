import binascii
import json
from datetime import datetime

from Crypto.Hash import keccak, SHA256
from Crypto.Signature import DSS
from cryptography import calculate_hash

class Transaction:
    def __init__(self, sender, receiver_address: bytes, amount: int):
        self.sender = sender
        self.receiver_address = receiver_address
        self.amount = amount
        self.timestamp = datetime.now()
        self.signature = ""

    def generate_transaction_data(self) -> dict:
        return {
            "sender": str(self.sender.address),
            "receiver": str(self.receiver_address),
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
        # self.signature = binascii.hexlify(signature).decode("utf-8")
        # print("POTPIS TEST 2: " + str(self.signature))
        # print("PRIVAT TEST 2: " + str(self.sender.private_key))

    def send(self):
        return {
            "sender": self.sender.address,
            "receiver": self.receiver_address,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "signature": self.signature
        }