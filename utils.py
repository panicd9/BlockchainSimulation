from cryptography import calculate_hash


def address_from_public_key(public_key):
    public_key = public_key.export_key(format='DER')
    _hash = calculate_hash(public_key)
    address = _hash[-40:]
    return address
