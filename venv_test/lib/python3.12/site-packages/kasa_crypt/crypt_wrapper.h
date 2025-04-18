

#include <stdint.h>
#include <stdio.h>
#include <string.h>


void _encrypt_into(const char * unencrypted, char * encrypted, unsigned long length) {
    uint8_t unencrypted_byte;
    uint8_t key = 171;
    for(unsigned i = 0; i < length; i++) {
        unencrypted_byte = unencrypted[i];
        key = key ^ unencrypted_byte;
        encrypted[i] = key;
    }
}
void _decrypt_into(const char * encrypted, char * unencrypted, unsigned long length) {
    uint8_t unencrypted_byte;
    uint8_t encrypted_byte;
    uint8_t key = 171;
    for(unsigned i = 0; i < length; i++) {
        encrypted_byte = encrypted[i];
        unencrypted_byte = key ^ encrypted_byte;
        key = encrypted_byte;
        unencrypted[i] = unencrypted_byte;
    }
}
