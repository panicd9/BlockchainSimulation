import requests
from Crypto.PublicKey import ECC

from cryptography import calculate_hash


# from transaction import Transaction


class Wallet:
    def __init__(self, private_key: ECC.EccKey, public_key: bytes, address: bytes):
        self.transaction_id = 0
        self.private_key = private_key
        self.public_key = public_key
        self.address = address
        # self.node = Node(None, None, None)

def import_wallet_from_file(private_key: ECC.EccKey):
    public_key = private_key.public_key().export_key(format='DER')
    # print(private_key.public_key().pointQ.size_in_bits())
    _hash = calculate_hash(public_key)
    address = _hash[-40:]
    public_key_pem = private_key.public_key().export_key(format='PEM')
    return Wallet(private_key, public_key_pem, address)


def initialize_wallet():
    private_key = ECC.generate(curve='P-256')
    public_key = private_key.public_key().export_key(format='DER')
    _hash = calculate_hash(public_key)
    address = _hash[-40:]
    public_key_pem = ECC.import_key(public_key).export_key(format='PEM')
    return Wallet(private_key, public_key_pem, address)
