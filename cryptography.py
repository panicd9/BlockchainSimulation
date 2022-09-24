import json
from Crypto.Hash import keccak


def calculate_hash(data: bytes) -> str:
    h = keccak.new(digest_bits=256)
    h.update(data)
    return h.hexdigest()

