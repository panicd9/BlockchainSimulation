import copy
import json
from typing import List

from constants import REWARD_AMOUNT, DIFFICULTY
from cryptography import calculate_hash
from merkle_tree import build_merkle_tree
from transaction import Transaction
from transaction_validation import is_transaction_valid


class BlockHeader:
    def __init__(self, block_id: int, previous_block_hash: str, timestamp: float, merkle_root: str):
        self.id = block_id
        self.previous_block_hash = previous_block_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.nonce = ""

    def get_hash(self) -> str:
        header_data = {
            "id": self.id,
            "merkle_root_hash": self.merkle_root,
            "timestamp": self.timestamp,
            "previous_block_hash": self.previous_block_hash,
            "nonce:": self.nonce
        }
        header_data_bytes = json.dumps(header_data, indent=4).encode('utf-8')
        return calculate_hash(header_data_bytes)

    def to_string(self) -> str:
        header_data = {
            "id": self.id,
            "merkle_root_hash": self.merkle_root,
            "timestamp": self.timestamp,
            "previous_block_hash": self.previous_block_hash,
            "nonce:": self.nonce
        }
        header_data_string = json.dumps(header_data, indent=4)
        return header_data_string


class Block:
    def __init__(self, header: BlockHeader, transactions: List[Transaction], previous_block=None):
        self.header = header
        self.transactions = transactions
        self.previous_block = previous_block

        if self.previous_block:
            self.header.previous_block_hash = previous_block.header_hash

        self.header_hash = None

    def proof_of_work_block(self, node_name: str, miner_address: str):

        # Validate transactions and remove invalid!
        valid_transactions = [t for t in self.transactions if is_transaction_valid(t, self)]
        # print(valid_transactions)
        header = copy.deepcopy(self.header)

        block = Block(header, valid_transactions, previous_block=self.previous_block)

        print("PRETHODNI HES BLOKA:::: " + str(block.header.previous_block_hash))
        # Reward for lucky miner!
        reward_transaction = Transaction("Coinbase", miner_address, REWARD_AMOUNT)
        block.transactions.append(reward_transaction)

        # Build new merkle root!
        merkle_root_node = build_merkle_tree(block.transactions)
        block.header.merkle_root = merkle_root_node.value

        # Include previous block hash!
        # if block.previous_block:
        #     block.header.previous_block_hash = block.previous_block.header.hash

        header.nonce = 0
        hash_to_find = calculate_hash(header.to_string())
        while hash_to_find[0:DIFFICULTY] != DIFFICULTY * "0":
            if self.header.nonce != "":
                print(f"{node_name} lost this block!\n")
                return
            # print(hash_to_find[0:3])
            hash_to_find = calculate_hash(header.to_string())
            # print("Nonce:" + str(nonce))
            # print(hash_to_find)
            header.nonce = header.nonce + 1

        self.header.nonce = header.nonce
        self.header_hash = hash_to_find
        self.header.merkle_root = merkle_root_node.value
        self.transactions = block.transactions

        if self.previous_block:
            self.header.previous_block_hash = block.previous_block.header_hash

        print(f"{node_name} found hash!\n"
              f"Block id: {self.header.id}     Nonce: {self.header.nonce}     Hash: {self.header_hash}\n"
              f"Header:{self.header.to_string()}\n")

    def __str__(self):
        to_string = "Header: \n\t" + \
                    self.header.to_string() + \
                    "\nTransactions:\n" + \
                    str(self.transactions) + \
                    "\n"
        return to_string
