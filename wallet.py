import base58
import requests
from Crypto.PublicKey import ECC, RSA
import base64
import secrets

from tinyec import ec, registry

from cryptography import calculate_hash
from node import Node
from transaction import Transaction


class Wallet:
    def __init__(self, private_key: ECC.EccKey, public_key: bytes, address: base64):
        self.private_key = private_key
        self.public_key = public_key
        self.address = address
        self.node = Node(None)

    def send_transaction(self, transaction: Transaction) -> requests.Response:
        transaction.sign()
        return self.node.send_transaction(transaction.generate_transaction_data())

def import_wallet_from_file(private_key: ECC.EccKey):
    public_key = private_key.public_key().export_key(format='DER')
    _hash = calculate_hash(public_key)
    address = _hash[-40:]
    public_key_pem = private_key.public_key().export_key(format='PEM')
    return Wallet(private_key, public_key_pem, address)


def initialize_wallet():
    private_key = ECC.generate(curve='P-256')
    # print(private_key.export_key(format='DER'))
    # print(private_key.public_key().export_key(format='DER'))
    public_key = private_key.public_key().export_key(format='DER')
    # print("TESTIRANJE! : ")
    # print(public_key)
    _hash = calculate_hash(public_key)
    # print(_hash)
    address = _hash[-40:]
    # print('Adresa: ' + address)
    public_key_pem = ECC.import_key(public_key).export_key(format='PEM')
    return Wallet(private_key, public_key_pem, address)

# def initialize_wallet():
#     ecc_curve = registry.get_curve('secp256r1')
#
#     print(ecc_curve)
#     private_key = secrets.randbelow(ecc_curve.field.n)
#     public_key = private_key * ecc_curve.g
#     print("private key:", private_key)
#     print("public key:", public_key)


# `private_key = ec.generate_private_key(ec.SECP256K1())
#
# public_key = private_key.public_key()
# vals=public_key.public_numbers()
# enc_point=binascii.b2a_hex(vals.encode_point()).decode()
# print (f"\nPublic key encoded point: {enc_point} \nx={enc_point[2:(len(enc_point)-2)//2+2]} \ny={enc_point[(len(enc_point)-2)//2+2:]}")`


# RSA VARIJANTA

# def initialize_wallet():
#     private_key = RSA.generate(2048)
#     print(private_key.export_key())
#     print(private_key.public_key().export_key())
#     public_key = private_key.publickey().export_key()
#     hash_1 = calculate_hash(public_key)
#     hash_2 = calculate_hash(hash_1)
#     address = base58.b58encode(hash_2)
#     return Address(private_key, public_key, address)
