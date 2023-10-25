"""Crypto module for acting with needed cryptography functions"""
from Crypto.PublicKey import ECC


def key_pair_gen():
    """Function that geenrates key pair"""

    key = ECC.generate(curve="NIST P-521")
    # encrypted_key = key.export_key(protection='PBKDF2WithHMAC-SHA1AndDES-EDE3-CBC',
    #                                format='DER')
    return key
