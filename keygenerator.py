"""
Using Fernet to generate a random key.
 """
from cryptography.fernet import Fernet

def key_gen(*args):
    """Generate a key with Fernet and saves it to a file"""
    key = Fernet.generate_key()
    save_file = args[0]

    with open(f"{save_file}.key", "wb") as key_file:
        key_file.write(key)
    print('---------------------------------')
    print(f"Key saved as: {save_file}.key")
    print(f"Key: {key.decode()}\n")
