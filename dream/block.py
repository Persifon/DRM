"""This moodule realise Block class and his method 
to storing information about transaction/raw data"""
import datetime

from Crypto.Hash import BLAKE2b
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

class Block:
    """Class that reaalize block structurre"""
    def __init__(self) -> None:
        self.data: str = ""
        self.previous_hashs: list[str] = [""]
        self.timestamp: datetime.datetime = datetime.datetime.now()
        self.nonce: int = 0
        self.hash: str = ""
        self.poster: str | bytes = ""
        self.sign: bytes = b''

    def calculate_hash(self) -> str:
        """Method that calculate hash of block"""
        blake = BLAKE2b.new()
        blake.update(str(self.data).encode('utf-8') +
            str(self.previous_hashs).encode('utf-8') +
            str(self.timestamp).encode('utf-8') +
            str(self.nonce).encode('utf-8'))
        self.hash = blake.hexdigest()
        return self.hash

    def sign_block(self, private_key: str, ) -> bytes:
        """Sign a block with private key"""
        with open(private_key, encoding='utf-8') as pk:
            key = ECC.import_key(pk.read()) #read private key
            signer = DSS.new(key, 'fips-186-3')
            signature = signer.sign(self.hash)
            self.sign = signature
            self.poster = key.public_key().export_key()
            return signature

    def is_sign_valid(self):
        """Check is sign valid"""
        key = ECC.import_key(self.poster)
        block_hash = self.calculate_hash()
        verifier = DSS.new(key, 'fips-186-3')
        try:
            verifier.verify(block_hash, self.sign)
            return True
        except ValueError:
            return False

    def __repr__(self):
        return f"{self.data}, {self.previous_hashs}, {self.nonce}"

# просто берем и при постинге блока просим 3 рандомных людей нагенерить рандомных данных и скинуть постеру, постер должен подписать данные своим ключём, затем мы скидываем блок бате (выбранному proof of history консенсусом челу) и тот проделывает те же самые действия. Таким образом мы защищаемся от двойных трат, ведь сделать перевод может исключительно владелец приватного ключа.
