"""
This moodule realise Block class and his method 
to storing information about transaction/raw data
"""

import datetime

from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS


class Block:
    """Class that realize block structurre"""

    def __init__(self, previous_hashs: list[str]) -> None:
        self.data: str
        self.previous_hashs = previous_hashs
        self.timestamp: datetime.datetime = datetime.datetime.now()
        self.nonce: int = 0
        self.hash: str = ""
        self.poster: ECC.EccKey
        self.sign: bytes = b''
        self.difficulty = 0

    def _push(self, data: str, key: ECC.EccKey):
        self.data = data
        
        self._calculate_hash(key)
        self._sign_block(key)
        return self.hash

    def _pushrd(self, data: str, privkey: str):
        """This function send some quantity to receiver"""
        
        return self._push(data, privkey)

    def _calculate_hash(self, key) -> str:
        """Method that calculate hash of block"""

        # with open(privkey, encoding='utf-8') as pk:
        #     key = ECC.import_key(pk.read()) #read private key
        self.poster = key.public_key()

        sha = SHA256.new()
        sha.update(str(self.data).encode('utf-8') +
            str(self.previous_hashs).encode('utf-8') +
            str(self.timestamp).encode('utf-8') +
            str(self.poster).encode('utf-8') +
            str(self.nonce).encode('utf-8'))
        self.hash = sha.hexdigest()
        return self.hash

    def _sign_block(self, key: ECC.EccKey) -> bytes:
        """Sign a block with private key"""

        if self.hash != "":
            signer = DSS.new(key, 'fips-186-3')
            self.sign = signer.sign(self.hash)
            return self.sign
        else:
            self._calculate_hash()
            return self._sign_block()

    def _is_sign_valid(self):
        """Check is sign valid"""

        key = ECC.import_key(self.poster)
        block_hash = self._calculate_hash()
        verifier = DSS.new(key, 'fips-186-3')
        try:
            verifier.verify(block_hash, self.sign)
            return True
        except ValueError:
            return False
    
    def mine(self):
        while self.hash[ : self.difficulty - 1] != ("0" * self.difficulty):
            self._calculate_hash
            self.nonce += 1
    
    def __repr__(self):
        return self.data, self.hash, self.nonce, self.poster, self.previous_hashs, self.sign, self.timestamp

    def __str__(self):
        return f"{self.poster}: {self.data}, {self.hash}, {self.sign}, {self.timestamp}"

# просто берем и при постинге блока просим 3 рандомных людей нагенерить рандомных данных и скинуть постеру, постер должен подписать данные своим ключём, затем мы скидываем блок бате (выбранному proof of history консенсусом челу) и тот проделывает те же самые действия. Таким образом мы защищаемся от двойных трат, ведь сделать перевод может исключительно владелец приватного ключа.