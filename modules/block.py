import datetime
import hashlib 


class Block:
    def __init__(self) -> None:
        self.data: str = ""
        self.previous_hashs: list[str] = [""]
        self.timestamp: datetime.datetime = datetime.datetime.now()
        self.nonce: int = 0
        self.hash: str = ""
        self.sign = '' # TODO: понятия не имею как реализовывать подписание блока, ведь нативных либ для таких штук в python просто нет, скорее всего буду писать бииблиотеку на golang для сети и криптобиблиотеку, вообще похоже что придется юзать не всроенные в python хэш функции, но я пока думаю.
    
    def calculate_hash(self):
        blake = hashlib.blake2b()
        blake.update(str(self.data).encode('utf-8') + 
            str(self.previous_hashs).encode('utf-8') + 
            str(self.timestamp).encode('utf-8') + 
            str(self.nonce).encode('utf-8'))
        self.hash = blake.hexdigest()
        return self.hash
    

    def __repr__(self):
        return f"{self.data}, {self.previous_hashs}, {self.nonce}"

"""
просто берем и при постинге блока просим 3 рандомных людей нагенерить рандомных данных и скинуть постеру, постер должен подписать данные своим ключём, затем мы скидываем блок бате (выбранному proof of history консенсусом челу) и тот проделывает те же самые действия. Таким образом мы защищаемся от двойных трат, ведь сделать перевод может исключительно владелец приватного ключа.
"""