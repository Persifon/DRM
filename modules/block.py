import datetime
import hashlib 
from ctypes import c_longdouble

class Block:
    def __init__(self) -> None:
        self.data: str
        self.previous_hashs: list[str]
        self.timestamp: datetime.datetime = datetime.datetime.now()
        self.nonce: int
        self.hash: str
        self.sign = '' # TODO: понятия не имею как реализовывать подписание блока, ведь нативных либ для таких штук в python просто нет, скорее всего буду писать бииблиотеку на golang для сети и криптобиблиотеку, вообще похоже что придется юзать не всроенные в python хэш функции, но я пока думаю.


    # скорее всего я не буду юзать эту функцию, но пусть пока повесит здесь.
    #
    # def mine_block(self, target_difficulty: str):
    #     while self.hash[:len(target_difficulty)] != target_difficulty:
    #         self.nonce += 1
    #         self.hash = self.calculate_hash()
    #     return self.hash
    

    def send(self, sender: str, receiver: str, quantity: c_longdouble):
        self.data = f"{sender}:{receiver}:{quantity}"
        hash = self._calculate_hash(self.data, self.previous_hashs, self.nonce, self.timestamp)
        return hash
    

    def push_raw_data(self, raw_data:str):
        self.data = raw_data
        hash = self._calculate_hash(self.data, self.previous_hashs, self.nonce, self.timestamp)
        return hash
    

    @staticmethod
    def _calculate_hash(data: str, previous_hashs: list[str], nonce: int, timestamp: datetime.datetime):
        blake = hashlib.blake2b()
        blake.update(str(data).encode('utf-8') + 
            str(previous_hashs).encode('utf-8') + 
            str(timestamp).encode('utf-8') + 
            str(nonce).encode('utf-8'))
        return blake.hexdigest()
    

    def __repr__(self):
        return f"{self.data}, {self.previous_hashs}, {self.nonce}"

"""
просто берем и при постинге блока просим 3 рандомных людей нагенерить рандомных данных и скинуть постеру, постер должен подписать данные своим ключём, затем мы скидываем блок бате (выбранному proof of history консенсусом челу) и тот проделывает те же самые действия. Таким образом мы защищаемся от двойных трат, ведь сделать перевод может исключительно владелец приватного ключа.
"""