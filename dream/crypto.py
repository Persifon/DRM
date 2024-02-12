"""Crypto module for acting with needed cryptography functions"""
from oqs import Signature


def key_pair_gen(sigalg = "Dilithium5") -> dict[str, bytes]:
    """Function that generate key pair"""

    with Signature(sigalg) as client:
        pk = client.generate_keypair()
        sk = client.export_secret_key()
        
    return {
        'pk': pk,
        'sk': sk
    }