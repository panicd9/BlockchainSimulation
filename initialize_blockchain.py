from datetime import datetime

from Crypto.PublicKey import ECC

from block import Block, BlockHeader
from merkle_tree import build_merkle_tree
from transaction import Transaction
from wallet import import_wallet_from_file


def initialize_blockchain():

    f1 = open('./wallets/wallet_A_private.der', 'rb')
    f2 = open('./wallets/wallet_B_private.der', 'rb')
    f3 = open('./wallets/wallet_C_private.der', 'rb')
    f4 = open('./wallets/wallet_D_private.der', 'rb')
    f5 = open('./wallets/wallet_E_private.der', 'rb')
    f6 = open('./wallets/wallet_F_private.der', 'rb')

    wallets = []
    wallet_A = import_wallet_from_file(ECC.import_key(f1.read()))
    wallet_B = import_wallet_from_file(ECC.import_key(f2.read()))
    wallet_C = import_wallet_from_file(ECC.import_key(f3.read()))
    wallet_D = import_wallet_from_file(ECC.import_key(f4.read()))
    wallet_E = import_wallet_from_file(ECC.import_key(f5.read()))
    wallet_F = import_wallet_from_file(ECC.import_key(f6.read()))
    wallets.append(wallet_A)
    wallets.append(wallet_B)
    wallets.append(wallet_C)
    wallets.append(wallet_D)
    wallets.append(wallet_E)
    wallets.append(wallet_F)

    transactions0 = [Transaction(wallet_A, wallet_B.address, 40), Transaction(wallet_B, wallet_C.address, 60),
                     Transaction(wallet_C, wallet_D.address, 20), Transaction(wallet_A, wallet_D.address, 100),
                     Transaction(wallet_F, wallet_B.address, 110), Transaction(wallet_A, wallet_E.address, 70)]

    transactions1 = [Transaction(wallet_A, wallet_C.address, 20), Transaction(wallet_A, wallet_C.address, 60),
                     Transaction(wallet_C, wallet_E.address, 40), Transaction(wallet_F, wallet_D.address, 10),
                     Transaction(wallet_F, wallet_E.address, 20), Transaction(wallet_C, wallet_E.address, 90)]

    transactions2 = [Transaction(wallet_A, wallet_C.address, 40), Transaction(wallet_E, wallet_C.address, 80),
                     Transaction(wallet_C, wallet_D.address, 20), Transaction(wallet_A, wallet_F.address, 70),
                     Transaction(wallet_E, wallet_B.address, 60), Transaction(wallet_A, wallet_D.address, 50)]

    # print(transactions2)

    timestamp_0 = datetime.timestamp(datetime.fromisoformat('2011-11-04 00:05:23.111'))
    # merkle_root_0 = build_merkle_tree(transactions0)
    block_header_0 = BlockHeader(0, None, timestamp_0, None)

    block_0 = Block(
        header=block_header_0,
        transactions=transactions0,
        previous_block=None
    )

    timestamp_1 = datetime.timestamp(datetime.fromisoformat('2011-11-07 00:05:19.222'))
    # merkle_root_1 = build_merkle_tree(transactions1)
    block_header_1 = BlockHeader(1, None, timestamp_1, None)
    block_1 = Block(
        header=block_header_1,
        transactions=transactions1,
        previous_block=block_0
    )

    timestamp_2 = datetime.timestamp(datetime.fromisoformat('2011-11-07 00:05:19.222'))
    # merkle_root_2 = build_merkle_tree(transactions2)
    block_header_2 = BlockHeader(2, None, timestamp_2, None)
    block_2 = Block(
        header=block_header_2,
        transactions=transactions2,
        previous_block=block_1
    )

    return block_2, wallets
