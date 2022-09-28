import binascii
import json

from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS


def verify_signature(transaction):
    transaction_data = bytearray(json.dumps(transaction.generate_transaction_data(), indent=4).encode('utf-8'))
    # print(transaction_data)
    transaction_hash = SHA256.new(transaction_data)
    # print("PUBLIC TEST 1: " + str(public_key))
    # print("HASH TEST 1: " + str(transaction_hash.hexdigest()))
    # print("KLJUC 1: " + str(public_key))
    # print(transaction.sender)
    # print(transaction.signature)
    # print(transaction_hash)
    # print(transaction.sender)
    try:
        # print(transaction)
        # print("AAA")
        # print(type(transaction.signature))
        public_key = ECC.import_key(transaction.sender.public_key)
        DSS.new(public_key, 'fips-186-3').verify(transaction_hash, transaction.signature)
        return True
    except Exception as e:
        print(e)
        return False


def validate_funds(head_block, sender_address: bytes, amount: int) -> bool:
    sender_balance = 0
    current_block = head_block
    while current_block:
        for transaction in current_block.transactions:
            if transaction.sender.address == sender_address:
                sender_balance = sender_balance - transaction.amount
            if transaction.receiver_address == sender_address:
                sender_balance = sender_balance + transaction.amount
        current_block = current_block.previous_block
    if amount <= sender_balance + 1000:
        return True
    else:
        return False


def is_transaction_valid(transaction, head_block):
    # print(transaction.sender)
    return verify_signature(transaction) and \
           validate_funds(head_block, transaction.sender.address, transaction.amount)
