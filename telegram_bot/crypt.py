import base64

from Crypto.Cipher import AES

IV = b"1029180179461904"


def get_cipher_suite(key):
    return AES.new(key, AES.MODE_CFB, IV)


def encrypt(data, key):
    encoded = get_cipher_suite(key).encrypt(data)
    encoded = base64.b64encode(encoded).decode('utf-8')
    return encoded


def decrypt(data, key):
    data = base64.b64decode(data.encode('utf-8'))
    return get_cipher_suite(key).decrypt(data)
