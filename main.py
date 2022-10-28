import threading
from initialize_blockchain import initialize_blockchain
from node import Node

if __name__ == "__main__":

    head_block, wallets = initialize_blockchain()

    blockchain_from_end = []

    current_block = head_block
    while current_block:
        blockchain_from_end.append(current_block)
        current_block = current_block.previous_block

    blockchain_from_start = list(reversed(blockchain_from_end))

    nodes = []
    threads = []
    for i in range(3):
        nodes.append(Node(head_block, f"Node {i}", wallets[i].address))
        threads.append(threading.Thread(target=nodes[i].start_pow, args=(blockchain_from_start,)))
        threads[i].start()

    for thread in threads:
        thread.join()

    for b in blockchain_from_start:
        print(str(b))

    # for block in blockchain_from_start:
    #     block.proof_of_work_block()

    # f1 = open('./wallets/wallet_A_private.der', 'rb')
    # f2 = open('./wallets/wallet_B_private.der', 'rb')
    # f3 = open('./wallets/wallet_C_private.der', 'rb')
    # f4 = open('./wallets/wallet_D_private.der', 'rb')
    # f5 = open('./wallets/wallet_E_private.der', 'rb')
    # f6 = open('./wallets/wallet_F_private.der', 'rb')
    #
    # wallet_A = import_wallet_from_file(ECC.import_key(f1.read()))
    # wallet_B = import_wallet_from_file(ECC.import_key(f2.read()))
    # wallet_C = import_wallet_from_file(ECC.import_key(f3.read()))
    # wallet_D = import_wallet_from_file(ECC.import_key(f4.read()))
    # wallet_E = import_wallet_from_file(ECC.import_key(f5.read()))
    # wallet_F = import_wallet_from_file(ECC.import_key(f6.read()))
    #
    # f1.close()
    # f2.close()
    # f3.close()
    # f4.close()
    # f5.close()
    # f6.close()

    # _transaction = Transaction(wallet_A, wallet_B.public_key, 20)
    # _transaction.sign()

    # _node = Node(head_block)
    # _node.proof_of_work_test()

    # # print("POTPIS TEST 1: " + transaction.signature)
    # print("PODACI TEST 1: " + str(bytearray(json.dumps(transaction.generate_transaction_data(), indent=4).encode('utf-8'))))
    # boolean = node.verify_signature(wallet1.public_key, transaction.signature,  bytearray(json.dumps(transaction.generate_transaction_data(), indent=4).encode('utf-8')))
    # #
    # print(boolean)
    # print("\n\n ajmo")
    #
    # key = ECC.generate(curve='P-256')
    # h = SHA256.new(b"123")
    # signer = DSS.new(key, 'fips-186-3')
    # signature = signer.sign(h)
    # verifier = DSS.new(key.public_key(), 'fips-186-3')
    # verifier.verify(h, signature)
    # print(key)
    # print(key.public_key())
