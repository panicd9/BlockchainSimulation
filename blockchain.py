import main


class Blockchain:
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []

    def append_block(self, block: main.Block):
        self.chain.append(block)

    def proof_of_work(self):
        for block in self.chain:
            main.proof_of_work_block(block)
