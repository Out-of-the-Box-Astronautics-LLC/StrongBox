__version__ = "0.5.0"

from struct import Struct

_pack_header = Struct(">I").pack

try:
    from ._crypt_impl import decrypt
    from ._crypt_impl import encrypt as _encrypt
except ImportError:
    from .python_impl import decrypt_pure_python as decrypt
    from .python_impl import encrypt_pure_python as _encrypt


def encrypt(string: str) -> bytes:
    """Encrypt."""
    encoded = string.encode("utf-8")
    return _pack_header(len(encoded)) + _encrypt(encoded)


__all__ = ["encrypt", "decrypt"]
