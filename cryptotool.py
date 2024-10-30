""" 
argparse module providing the ability to take arguments in the commandline.
os module provides a portable way of using operating system dependent functionality.
Fernet from cryptography to encrypt and decrypt files.
"""
import argparse
import os

from cryptography.fernet import Fernet

def encrypt(message, key):
    """Encrypting a file with a key given from argparse"""
    with open(key, "rb") as key_file:
        key = key_file.read()
    print('-------------------------------------')
    print(f"Key: {key.decode()}") #.decode() removes the binary format

    with open(message, 'r') as message_file:
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
        with open(args[0], 'w') as save_file:
            save_file.write(plain_text_decoded)
            print(f"\nDecryption saved as a copy: {args[0]}")


def main():
    """Running argparse to call functions"""
    parser = argparse.ArgumentParser(description="Crypto Tool")
    parser.add_argument("File", help="Enter a file")
    parser.add_argument("Key", help="Enter a valid key")

    group = parser.add_mutually_exclusive_group() #Makes sure you cant use -d &-e at the same time.
    group.add_argument("-d", "--decrypt", action="store_true", help="decrypt a file with a key")
    group.add_argument("-e", "--encrypt", action="store_true", help="encrypt a file with a key")

    parser.add_argument("-s", "--save", action="store_true", help="save decryption to a file")

    args = parser.parse_args()

    if os.path.exists(args.File) and os.path.exists(args.Key):
        if args.encrypt:
            encrypt(args.File, args.Key)
        elif args.decrypt:
            if args.save:
                print('-------------------------------------')
                save_file = input("Choose a savefile: ")
                decrypt(args.File, args.Key, save_file)
            else:
                decrypt(args.File, args.Key)

    elif os.path.exists(args.File):
        print(f"Cannot find: {args.Key}")

    elif os.path.exists(args.Key):
        print(f"Cannot find: {args.File}")
    else:
        print("Cannot find files")


if __name__ == "__main__":
    main()
