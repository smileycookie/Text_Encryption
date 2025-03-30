# -*- coding: utf-8 -*-
"""Text Encryption/Decryption Tool.ipynb

#Created By: Ripunjay Singh
#Creation Date: 11-March-2025
#Last Modified: 29-March-2025
#LinkedIn ID: //www.linkedin.com/in/curicodemoore/

# **Text Encryption**
"""
"""## **Importing Different Libraries**"""

!pip install pycryptodome #Installing Pycryptodome for
!pip install colorama #Installing Colorama for
import base64 #Data Encoding/Decoding
import os #Operating System Interaction
import time #Time Management
import sys #System-Specific Functions
from Crypto.Cipher import AES, DES, PKCS1_OAEP #Encryption and Decryption
from Crypto.PublicKey import RSA #
from Crypto.Util.Padding import pad, unpad #Data Padding:
from colorama import init, Fore, Style #Colored Terminal Output

"""## **Function to animate text for better UI experience**"""

def animate_text(text, delay=0.05):
    """Prints text one character at a time."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

"""## **Base64 encoding with encryption method obfuscation**"""

def custom_encode(data: bytes, algorithm: str) -> str:
    encoded = base64.b64encode(data).decode('utf-8').rstrip('=')
    if algorithm == 'AES':
        return encoded + "="
    elif algorithm == 'DES':
        return encoded + "=="
    elif algorithm == 'RSA':
        return encoded
    return encoded

"""## **Base64 decoding with algorithm detection**"""

def custom_decode(encoded: str) -> (bytes, str):
    if encoded.endswith("=="):
        algorithm = 'DES'
        encoded = encoded[:-2]
    elif encoded.endswith("="):
        algorithm = 'AES'
        encoded = encoded[:-1]
    else:
        algorithm = 'RSA'
    missing_padding = len(encoded) % 4
    if missing_padding:
        encoded += '=' * (4 - missing_padding)
    return base64.b64decode(encoded), algorithm

"""## **AES Encryption/Decryption**"""

def aes_encrypt(plaintext: str, key: bytes) -> str:
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_bytes = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    data = iv + encrypted_bytes
    return custom_encode(data, 'AES')

def aes_decrypt(data: bytes, key: bytes) -> str:
    iv, ciphertext = data[:16], data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_bytes = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_bytes.decode()

"""## **DES Encryption/Decryption**"""

def des_encrypt(plaintext: str, key: bytes) -> str:
    iv = os.urandom(8)
    cipher = DES.new(key, DES.MODE_CBC, iv)
    encrypted_bytes = cipher.encrypt(pad(plaintext.encode(), DES.block_size))
    data = iv + encrypted_bytes
    return custom_encode(data, 'DES')

def des_decrypt(data: bytes, key: bytes) -> str:
    iv, ciphertext = data[:8], data[8:]
    cipher = DES.new(key, DES.MODE_CBC, iv)
    decrypted_bytes = unpad(cipher.decrypt(ciphertext), DES.block_size)
    return decrypted_bytes.decode()

"""## **RSA Encryption/Decryption**"""

def rsa_encrypt(plaintext: str, public_key) -> str:
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_bytes = cipher.encrypt(plaintext.encode())
    return custom_encode(encrypted_bytes, 'RSA')

def rsa_decrypt(data: bytes, private_key) -> str:
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_bytes = cipher.decrypt(data)
    return decrypted_bytes.decode()

"""## **Automatic decryption with hidden algorithm detection**"""

def decrypt_with_hidden_tag(encoded_text: str, aes_key: bytes, des_key: bytes, rsa_private_key) -> str:
    decoded_data, algorithm = custom_decode(encoded_text)
    if algorithm == 'AES':
        return aes_decrypt(decoded_data, aes_key)
    elif algorithm == 'DES':
        return des_decrypt(decoded_data, des_key)
    elif algorithm == 'RSA':
        return rsa_decrypt(decoded_data, rsa_private_key)
    return "Unknown encryption method!"

"""## **Key Generation**"""

aes_key = b'1234567890123456'  # 16-byte key for AES
des_key = b'8bytekey'          # 8-byte key for DES
rsa_key = RSA.generate(2048)   # RSA 2048-bit key pair
rsa_public_key = rsa_key.publickey()
rsa_private_key = rsa_key

"""## **Main menu-driven program**"""

def main():
    while True:
        animate_text(Fore.CYAN + "==== Text Encryption/Decryption Tool ====" + Style.RESET_ALL)
        print("Choose an option:")
        print("1. Encrypt Text")
        print("2. Decrypt Text")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            text = input("Enter text to encrypt: ")
            print("\nSelect encryption method:")
            print("1. AES")
            print("2. DES")
            print("3. RSA")
            enc_choice = input("Enter your choice: ")

            if enc_choice == '1':
                encrypted_text = aes_encrypt(text, aes_key)
                print(Fore.GREEN + f"\nEncrypted Text (AES): {encrypted_text}" + Style.RESET_ALL)
            elif enc_choice == '2':
                encrypted_text = des_encrypt(text, des_key)
                print(Fore.GREEN + f"\nEncrypted Text (DES): {encrypted_text}" + Style.RESET_ALL)
            elif enc_choice == '3':
                encrypted_text = rsa_encrypt(text, rsa_public_key)
                print(Fore.GREEN + f"\nEncrypted Text (RSA): {encrypted_text}" + Style.RESET_ALL)
            else:
                print(Fore.RED + "Invalid choice!" + Style.RESET_ALL)
                continue  # Skip to next iteration of the loop

            print(Fore.MAGENTA + "Encryption done!" + Style.RESET_ALL)

        elif choice == '2':
            encrypted_text = input("Enter the encrypted text: ")
            decrypted_text = decrypt_with_hidden_tag(encrypted_text, aes_key, des_key, rsa_private_key)
            print(Fore.YELLOW + f"\nDecrypted Text: {decrypted_text}" + Style.RESET_ALL)
            print(Fore.MAGENTA + "Decryption done!" + Style.RESET_ALL)

        elif choice == '3':
            print(Fore.CYAN + "Exiting... Goodbye!" + Style.RESET_ALL)
            break  # Exit the loop properly

        else:
            print(Fore.RED + "Invalid choice! Please try again." + Style.RESET_ALL)

"""## **Run the program**"""

if __name__ == "__main__":
    main()
