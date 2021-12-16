# global const setting
jzy_appId= "wxb628d9e8ab4ac444"
jzy_appSecret= "2af58323c7bb1e34c65382a5e3e189cb"
frz_appId= "wxc7d83747281bfcc8"
frz_appSecret= "ccc50b8d77d28b11d5dee0164fd96b1b"
lsz_appId= "wxd658ab1f82314e2a"
lsz_appSecret= "815767c2cf0359f4910dee4136de0962"
ld_appId = "wxbec495af85714e3b"
ld_appSecret = "ae8c07f1c54cc187d46bb419d6469252"
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad 
secret_key = get_random_bytes(16)
# guard_appId = frz_appId
# guard_appSecret = frz_appSecret

guard_appId = jzy_appId
guard_appSecret = jzy_appSecret

# guest_appId = jzy_appId
# guest_appSecret = jzy_appSecret

guest_appId = jzy_appId
guest_appSecret = jzy_appSecret
remind_template="7oNPU5JtIAl73LkYMi2PFkPh-Eqf15h8qpRfA4YQVkM"
# key = get_random_bytes(16)
key = b'0123456789abcdef'
cipher = AES.new(key,AES.MODE_ECB)

guard_password="123456"

admin_password="123456"