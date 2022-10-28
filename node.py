class Node:
    def __init__(self, block, name, miner_address):
        self.name = name
        self.block = block
        self.miner_address = miner_address

    def proof_of_work_test(self):
        current_block = self.block
        blockchain_from_start = []
        while current_block:
            blockchain_from_start.append(current_block)
            current_block = current_block.previous_block
        blockchain_from_start = list(reversed(blockchain_from_start))

        for block in blockchain_from_start:
            block.proof_of_work_block()

    def start_pow(self, blocks):
        for block in blocks:
            block.proof_of_work_block(node_name=self.name, miner_address=self.miner_address)