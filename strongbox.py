"""
strongbox.py

A secure encryption and decryption utility for files and strings using the cryptography package.
Implements key derivation (PBKDF2HMAC) and symmetric encryption (Fernet).

Usage:
    Encrypt or decrypt files/strings from the command line:
        python strongbox.py encrypt --input <input_file> --output <output_file> --password <password>
        python strongbox.py decrypt --input <input_file> --output <output_file> --password <password>

Command-line arguments are handled with argparse.
"""

import base64
import argparse
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet, InvalidToken

# Constants
SALT_SIZE = 16  # bytes, for PBKDF2HMAC salt
KDF_ITERATIONS = 390000  # Number of PBKDF2 iterations (recommended: >= 100,000)


def derive_key(password: str, salt: bytes) -> bytes:
    """
    Derive a Fernet-compatible key from a password and salt using PBKDF2HMAC.

    Args:
        password (str): The user-supplied password.
        salt (bytes): A random salt for key derivation.

    Returns:
        bytes: A base64-encoded 32-byte key suitable for Fernet.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def encrypt_data(data: bytes, password: str) -> bytes:
    """
    Encrypt data using a password-derived key and Fernet symmetric encryption.

    Args:
        data (bytes): The plaintext data to encrypt.
        password (str): The password to derive the encryption key.

    Returns:
        bytes: The encrypted data, with the salt prepended (salt + ciphertext).
    """
    salt = os.urandom(SALT_SIZE)
    key = derive_key(password, salt)
    f = Fernet(key)
    ciphertext = f.encrypt(data)
    return salt + ciphertext  # Prepend salt for use in decryption


def decrypt_data(token: bytes, password: str) -> bytes:
    """
    Decrypt data using a password-derived key and Fernet symmetric encryption.

    Args:
        token (bytes): The encrypted data (salt + ciphertext).
        password (str): The password to derive the decryption key.

    Returns:
        bytes: The decrypted plaintext data.

    Raises:
        InvalidToken: If the password is incorrect or data is corrupted.
    """
    salt = token[:SALT_SIZE]
    ciphertext = token[SALT_SIZE:]
    key = derive_key(password, salt)
    f = Fernet(key)
    return f.decrypt(ciphertext)


def encrypt_file(input_path: str, output_path: str, password: str) -> None:
    """
    Encrypt a file and write the encrypted output to a new file.

    Args:
        input_path (str): Path to the plaintext input file.
        output_path (str): Path to write the encrypted file.
        password (str): Password for encryption.
    """
    with open(input_path, 'rb') as infile:
        data = infile.read()
    encrypted = encrypt_data(data, password)
    with open(output_path, 'wb') as outfile:
        outfile.write(encrypted)


def decrypt_file(input_path: str, output_path: str, password: str) -> None:
    """
    Decrypt an encrypted file and write the plaintext output to a new file.

    Args:
        input_path (str): Path to the encrypted input file.
        output_path (str): Path to write the decrypted file.
        password (str): Password for decryption.
    """
    with open(input_path, 'rb') as infile:
        token = infile.read()
    decrypted = decrypt_data(token, password)
    with open(output_path, 'wb') as outfile:
        outfile.write(decrypted)


def main():
    """
    Parse command-line arguments and perform encryption or decryption.
    """
    parser = argparse.ArgumentParser(
        description="Encrypt or decrypt files using password-based encryption (Fernet/PBKDF2HMAC)."
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Encrypt command
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt a file')
    encrypt_parser.add_argument('--input', required=True, help='Path to input file')
    encrypt_parser.add_argument('--output', required=True, help='Path to output (encrypted) file')
    encrypt_parser.add_argument('--password', required=True, help='Password for encryption')

    # Decrypt command
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt a file')
    decrypt_parser.add_argument('--input', required=True, help='Path to input (encrypted) file')
    decrypt_parser.add_argument('--output', required=True, help='Path to output (decrypted) file')
    decrypt_parser.add_argument('--password', required=True, help='Password for decryption')

    args = parser.parse_args()

    try:
        if args.command == 'encrypt':
            encrypt_file(args.input, args.output, args.password)
            print(f"File encrypted and saved to {args.output}")
        elif args.command == 'decrypt':
            decrypt_file(args.input, args.output, args.password)
            print(f"File decrypted and saved to {args.output}")
    except InvalidToken:
        print("ERROR: Invalid password or corrupted file. Decryption failed.")
        exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        exit(1)


if __name__ == "__main__":
    main()
