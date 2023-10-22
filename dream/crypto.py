"""Crypto module for acting with needed cryptography functions"""
from Crypto.PublicKey import ECC

def key_pair_gen():
    """Function that geenrates key pair"""
    key = ECC.generate('NIST P-521')
    encrypted_key = key.export_key(use_pkcs8=True, 
                                   protection='PBKDF2WithHMAC-SHA1AndDES-EDE3-CBC')
    return key.public_key().export_key(), encrypted_key
