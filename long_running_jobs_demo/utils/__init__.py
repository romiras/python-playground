import os

def random_hex_string(length=6):
    return os.urandom(length).hex()
