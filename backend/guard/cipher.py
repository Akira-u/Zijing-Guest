
from .const import *

def encrypt(raw):
    cipher_text = cipher.encrypt(pad(raw.encode(),AES.block_size))
    return str(cipher_text)

def decrypt(cipher_text):
    plaintext = cipher.decrypt(eval(cipher_text))
    return plaintext.decode()[:28]
