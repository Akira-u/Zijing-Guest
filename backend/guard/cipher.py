
from .const import *
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad 

key = b'0123456789abcdef'
cipher = AES.new(key,AES.MODE_ECB)

def encrypt(raw):
    cipher_text = cipher.encrypt(pad(raw.encode(),AES.block_size))
    return str(cipher_text)

def decrypt(cipher_text):
    plaintext = cipher.decrypt(eval(cipher_text))
    return plaintext.decode()[:28]
