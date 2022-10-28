import binascii
from Crypto.PublicKey import ECC
from utils import address_from_public_key


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
            "sender": '0x' + str(self.sender_address),
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
            "timestamp": str(self.timestamp),
            "signature": binascii.hexlify(self.signature).decode("utf-8")
        }

    def __str__(self):
        # public_key_ascii = ECC.import_key(self.sender.public_key).export_key(format='PEM')
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
