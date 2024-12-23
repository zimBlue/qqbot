import secrets
import string

def generate_random_key(length=16):
    characters = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(characters) for _ in range(length))
    return key