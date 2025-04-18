def encrypt_pure_python(unencrypted: bytes) -> bytearray:
    """Encrypt."""
    key = 171
    unencrypted_len = len(unencrypted)
    encrypted = bytearray(unencrypted_len)
    for idx, unencryptedbyte in enumerate(unencrypted):
        key = key ^ unencryptedbyte
        encrypted[idx] = key
    return encrypted


def decrypt_pure_python(string: bytes) -> str:
    """Decrypt."""
    key = 171
    result = bytearray(len(string))
    for idx, i in enumerate(string):
        a = key ^ i
        key = i
        result[idx] = a
    return result.decode()
