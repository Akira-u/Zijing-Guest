
from .const import *

def encrypt(raw):
    cipher_text = cipher.encrypt(pad(raw.encode(),AES.block_size))
    # print(cipher_text)
    # print(cipher2.decrypt(cipher_text))
    return str(cipher_text)

def decrypt(cipher_text):
    # print(eval(cipher_text))
    plaintext = cipher.decrypt(eval(cipher_text))
    # cipher2.update()
    # print(plaintext)
    # print(plaintext.decode()[:28])
    return plaintext.decode()[:28]


# cip=encrypt("123456")
# cip2=encrypt("6789")
# decrypt(cip)

# cip=encrypt("123456")
# decrypt(cip)