import json

from Crypto.Hash import keccak

import blockchain


def calculate_hash(data: bytes) -> str:
    h = keccak.new(digest_bits=256)
    h.update(data)
    return h.hexdigest()


class Block:
    def __init__(self, timestamp: float, transactions: str, previous_block=None):
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_block = previous_block

    @property
    def previous_block_hash(self):
        previous_block_hash = ""
        if self.previous_block:
            previous_block_hash = self.previous_block.hash
        return previous_block_hash

    @property
    def hash(self) -> str:
        block_data = {
            "transaction_data": self.transactions,
            "timestamp": self.timestamp,
            "previous_block_cryptographic_hash": self.previous_block_hash
        }
        block_data_bytes = json.dumps(block_data, indent=2).encode('utf-8')
        # block_data_bytes = json.dumps(block_data).encode('utf-8')
        print(block_data_bytes)
        return calculate_hash(block_data_bytes)

    def __str__(self):
        to_string = "Timestamp: \n\t" + \
                    str(self.timestamp) + \
                    "\nHash: \n\t" + \
                    self.hash + \
                    "\nTransactions:\n\t" + \
                    json.dumps(self.transactions) + \
                    "\n"
        return to_string


def proof_of_work_block(block: Block):
    nonce = 0
    data_to_hash = json.dumps(block.transactions) + str(nonce)
    hash_to_find = calculate_hash(data_to_hash.encode('utf-8'))
    while hash_to_find[0:4] != "0000":
        print(hash_to_find[0:4])
        data_to_hash = json.dumps(block.transactions) + str(nonce)
        hash_to_find = calculate_hash(data_to_hash.encode('utf-8'))
        print("Nonce:" + str(nonce))
        print(hash_to_find)
        nonce = nonce + 1


from datetime import datetime

transactions = []
transaction_data = {'from': 'Darko', 'to': 'Igor', 'value': '30', 'timestamp': '2011-11-04 00:05:23.111'}
transactions.append(transaction_data)
transaction_data = {'from': 'Igor', 'to': 'Stefan', 'value': '10', 'timestamp': '2012-11-07 00:05:13.222'}
transactions.append(transaction_data)
transaction_data = {'from': 'Stefan', 'to': 'Darko', 'value': '10', 'timestamp': '2013-11-09 00:11:13.333'}
transactions.append(transaction_data)
transaction_data = {'from': 'Darko', 'to': 'Stefan', 'value': '20', 'timestamp': '2014-11-04 00:05:23.111'}
transactions.append(transaction_data)
transaction_data = {'from': 'Stefan', 'to': 'Igor', 'value': '5', 'timestamp': '2015-11-07 00:05:13.222'}
transactions.append(transaction_data)
transaction_data = {'from': 'Stefan', 'to': 'Darko', 'value': '10', 'timestamp': '2016-11-09 00:11:13.333'}
transactions.append(transaction_data)

timestamp_0 = datetime.timestamp(datetime.fromisoformat('2011-11-04 00:05:23.111'))

block_0 = Block(
    transactions=transactions[0],
    timestamp=timestamp_0
)

timestamp_1 = datetime.timestamp(datetime.fromisoformat('2011-11-07 00:05:13.222'))
block_1 = Block(
    transactions=transactions[1],
    timestamp=timestamp_1,
    previous_block=block_0
)

timestamp_2 = datetime.timestamp(datetime.fromisoformat('2011-11-09 00:11:13.333'))
block_2 = Block(
    transactions=transactions[2],
    timestamp=timestamp_2,
    previous_block=block_1
)

if __name__ == "__main__":
    b = blockchain.Blockchain()
    b.append_block(block_0)
    b.append_block(block_1)
    b.append_block(block_2)

    print('--------------------------')
    print(block_0)
    print(block_1)
    print(block_2)
    print('--------------------------')

    b.proof_of_work()
