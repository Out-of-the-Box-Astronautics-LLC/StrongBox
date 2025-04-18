import cython

from libc.stdlib cimport free, malloc
from libc.string cimport strlen


cdef extern from "crypt_wrapper.h":
    void _encrypt_into(const char * unencrypted, char * encrypted, unsigned long length)
    void _decrypt_into(const char * encrypted, char * unencrypted, unsigned long length)

cdef void _decrypt(const char *encrypted, char **unencrypted, Py_ssize_t length):
    unencrypted[0] = <char *> malloc((length + 1) * sizeof(char))
    if not unencrypted[0]:
        return  # malloc failed
    _decrypt_into(encrypted, unencrypted[0], length)

cdef void _encrypt(const char *unencrypted, char** encrypted, Py_ssize_t length):
    encrypted[0] = <char *> malloc((length + 1) * sizeof(char))
    if not encrypted[0]:
        return  # malloc failed
    _encrypt_into(unencrypted, encrypted[0], length)

def encrypt(py_byte_string: bytes) -> bytes:
    cdef char* encrypted = NULL
    cdef Py_ssize_t length = len(py_byte_string)
    _encrypt(py_byte_string, &encrypted, length)
    try:
        return encrypted[:length]
    finally:
        free(encrypted)

def decrypt(string: bytes) -> str:
    cdef char* unencrypted = NULL
    cdef Py_ssize_t length = len(string)
    _decrypt(string, &unencrypted, length)
    try:
        return unencrypted[:length].decode('utf-8')
    finally:
        free(unencrypted)
