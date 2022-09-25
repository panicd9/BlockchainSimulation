import json
from Crypto.Hash import keccak


def calculate_hash(data) -> str:
    if type(data) == dict:
        data = json.dumps(data, indent=4)
    if type(data) == str:
        data = bytearray(data.encode('utf-8'))

    h = keccak.new(digest_bits=256)
    h.update(data)
    return h.hexdigest()

