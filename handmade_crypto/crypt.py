import handmade_crypto as hc
import sys
from os.path import exists

if exists("secret.key"):
    message = input("Your secret message: ")
    crypto_key = hc.read_file("secret.key")
    cipher = hc.xor_fn(message, crypto_key)
    print(f"Cipher text is: {cipher}")
    hc.write_file("ciphertext.txt", cipher)
    data = hc.read_file("ciphertext.txt")
    plain = hc.xor_fn(data, crypto_key)
    print(f"Decrypted text: {plain}")
else:
    key = hc.create_key()  # Key length is 1024 bytes long.
    print(f"Key generated: {key}")
    if hc.write_file("secret.key", key):
        print("Key is written to file.")
    else:
        print("Key has failed to write to file.")
        sys.exit(1)
