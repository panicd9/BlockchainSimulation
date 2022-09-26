from Crypto.PublicKey import ECC

from wallet import import_wallet_from_file

f1 = open('./wallets/wallet_A_private.der', 'rb')
f2 = open('./wallets/wallet_B_private.der', 'rb')
f3 = open('./wallets/wallet_C_private.der', 'rb')
f4 = open('./wallets/wallet_D_private.der', 'rb')
f5 = open('./wallets/wallet_E_private.der', 'rb')
f6 = open('./wallets/wallet_F_private.der', 'rb')

wallet_A = import_wallet_from_file(ECC.import_key(f1.read()))
wallet_B = import_wallet_from_file(ECC.import_key(f2.read()))
wallet_C = import_wallet_from_file(ECC.import_key(f3.read()))
wallet_D = import_wallet_from_file(ECC.import_key(f4.read()))
wallet_E = import_wallet_from_file(ECC.import_key(f5.read()))
wallet_F = import_wallet_from_file(ECC.import_key(f6.read()))