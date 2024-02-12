"""
This moodule realise Block class and his method 
to storing information about transaction/raw data
"""

from datetime import datetime
from hashlib import new

from oqs import Signature

class Block:
    """Class that realize block structurre"""

    def __init__(self, previous_hashs: list[str]) -> None:
        self.data: str
        self.previous_hashs = previous_hashs
        self.timestamp: datetime = datetime.now()
        self.nonce: int = 0
        self.hash: bytes = bytes()
        self.poster: bytes
        self.sign: bytes = b""
        self.difficulty = 0

    def _push(self, data: str, key: dict[str, bytes]) -> bytes:
        """Push data"""
        
        self.data = data
        self.poster = key['pk']
        self._calculate_hash()
        self._sign_block(key)
        
        return self.hash

    def _calculate_hash(self) -> bytes:
        """Method that calculate hash of block"""

        sha = new('sha512')
        sha.update(
            str(self.data).encode("utf-8")
            + str(self.previous_hashs).encode("utf-8")
            + str(self.timestamp).encode("utf-8")
            + str(self.poster).encode("utf-8")
            + str(self.nonce).encode("utf-8")
        )
        self.hash = sha.hexdigest().encode()
        
        return self.hash

    def _sign_block(self, key) -> bytes:
        """Sign a block with private key"""

        signer = Signature("Dilithium5", key['sk'])
        self.sign = signer.sign(self.hash)
        
        return self.sign

    def _is_sign_valid(self) -> bool:
        """Check is sign valid"""

        with Signature("Dilithium5") as verifier:
            is_valid = verifier.verify(self.hash, self.sign, self.poster)
        
        return is_valid

    def mine(self):
        """Mine block"""

        while self.hash[: self.difficulty - 1] != ("0" * self.difficulty):
            self._calculate_hash
            self.nonce += 1

        return self.nonce
    
    def __str__(self):
        return f"{self.poster}: {self.data}, {self.hash}, {self.sign}, {self.timestamp}"
