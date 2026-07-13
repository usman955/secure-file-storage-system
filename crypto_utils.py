# crypto_utils.py
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

KDF_ITERATIONS = 200_000
KDF_LEN = 32  # 256-bit key

def gen_salt(length: int = 16) -> bytes:
    return os.urandom(length)

def derive_key(password: bytes, salt: bytes) -> bytes:
    """
    Derive a symmetric key from password and salt using PBKDF2-HMAC-SHA256.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KDF_LEN,
        salt=salt,
        iterations=KDF_ITERATIONS
    )
    return kdf.derive(password)

def encrypt_bytes(plaintext: bytes, key: bytes):
    aes = AESGCM(key)
    nonce = os.urandom(12)
    ct = aes.encrypt(nonce, plaintext, None)
    return nonce, ct

def decrypt_bytes(nonce: bytes, ciphertext: bytes, key: bytes):
    aes = AESGCM(key)
    return aes.decrypt(nonce, ciphertext, None)
