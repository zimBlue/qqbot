import hashlib
import secrets
import string

def generate_random_key(length=16):
    characters = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(characters) for _ in range(length))
    return key

def md5(str):
    return hashlib.md5(str.encode("utf-8")).hexdigest()