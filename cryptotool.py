""" 
Fernet from cryptography to encrypt and decrypt files.
"""
import os

from cryptography.fernet import Fernet

def encrypt(message, key):
    """Encrypting a file with a key given from argparse"""
    with open(key, "rb") as key_file:
        key = key_file.read()
    print('-------------------------------------')
    print(f"Key: {key.decode()}") #.decode() removes the binary format

    with open(message, 'r', encoding='UTF-8') as message_file:
        message_content = message_file.read()
        message_content = message_content.encode() #.encode() changes the message to binary format

    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(message_content)
    print('-------------------------------------')
    print(f"Encrypted text: {cipher_text}")

    message_enc = f"{message.replace('.', '_')}.enc"
    os.replace(message, message_enc) #replace the plaintext file with the encrypted file

    with open(message_enc, "wb") as encoded_file:
        encoded_file.write(cipher_text)
        print('-------------------------------------')
        print(f"File: {message} > {message_enc}")

def decrypt(enc_message, key, *args):
    """Decrypting a file with a key and a optional save to file given from argparse"""
    with open(enc_message, "rb") as encoded_file:
        message = encoded_file.read()

    with open(key, "rb") as key_file:
        key = key_file.read()
    print('-------------------------------------')
    print(f"Key: {key.decode()}")

    cipher_suite = Fernet(key)

    plain_text = cipher_suite.decrypt(message)
    plain_text_decoded = plain_text.decode()

    print('-------------------------------------')
    print(f"Decrypted text:\n{plain_text_decoded}")
    print('-------------------------------------')
    if args:                           #saves the result to a file if chosen as an argument
        with open(args[0], 'w', encoding='UTF-8') as save_file:
            save_file.write(plain_text_decoded)
            print(f"\nDecryption saved as a copy: {args[0]}")
