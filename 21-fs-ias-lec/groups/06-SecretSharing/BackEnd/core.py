"""
::Export Module::
The core script contains all functions interfacing with the BACNetCore but not directly with other SecretSharing
related scripts. Other groups can import SecretSharing.BackEnd.core to make use of the functionality without getting
complications. core.py will be imported into actions.py and the UI can therefore interface with all functions
here as well. For example private messages should be implemented here.
"""

# BACnet imports

# import BACnetCore
# import BACnetTransport
import sneakernet.sneakernet_functions
from sneakernet import logMerge
from sneakernet import logStore


from Crypto.Cipher import AES
from Crypto.Hash import SHA256, HMAC
from Crypto.PublicKey import RSA
from enum import Enum
from os import urandom
from ast import literal_eval
import cbor2
import json

cType = Enum("Shard", "Request")


def pad(s):
    return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)


def event(type: str, receivers_pubkey=None, shard=None, auth_msg=None, index=None, keyid=None, text=None):
    # random HMAC cipher
    hash_key = urandom(16)
    hash_cipher = HMAC.new(hash_key, digestmod=SHA256)
    # Maybe whole content? New Field?

    content = {
        "TYPE": type.name,
        "SHARD": shard,
        "HASH": auth_msg,
        "INDEX": index,
        "KEYID": keyid,
        "RECV": receivers_pubkey,
        "TEXT": text
    }

    # random AES cipher
    aes_key = urandom(16)
    aes_iv = urandom(16)
    aes_cipher = AES.new(aes_key, AES.MODE_CBC, iv=aes_iv)

    # encrypt complete content as padded string
    encrypted_content = aes_cipher.encrypt(pad(json.dumps(content).encode("utf-8")))

    e = {
        "HMAC": receivers_pubkey.encrypt(hash_key).decode("utf-8"),
        "AES": receivers_pubkey.encrypt(aes_key).decode("utf-8"),
        "IV": aes_iv.decode("utf-8"),
        "CONTENT": encrypted_content.decode("utf-8")
    }

    return json.dumps(e)


def decrypt_event(event, private_key):
    """Decrypts a plaintext event."""
    e: dict = literal_eval(event)
    hash_key = private_key.decrypt(e["HMAC"].encode("utf-8"))
    aes_key = private_key.decrypt(e["AES"].encode("utf-8"))
    aes_iv = e["IV"].encode("utf-8")
    ciphertext = e["CONTENT"].encode("utf-8")
    del e

    # Authentication

    # Decryption
    plaintext_p = AES.new(aes_key, AES.MODE_CBC, aes_iv).decrypt(ciphertext)
    c: dict = json.loads(plaintext_p[:-plaintext_p[-1]].decode("utf-8"))
    t = cType(c["TYPE"])

    # Switch type in subroutines, return through this function eg
