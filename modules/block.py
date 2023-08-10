import datetime
import hashlib 
from ctypes import c_longdouble

class Block:
    def __init__(self) -> None:
        self.data = ""
        self.previous_hashs = 0
        self.timestamp = datetime.datetime.now()
        self.nonce = 0
        self.hash = ""
    
    def calculate_hash(self):
        blake = hashlib.blake2b()
        blake.update(str(self.data).encode('utf-8') + 
             str(self.previous_hashs).encode('utf-8') + 
             str(self.nonce).encode('utf-8'))
        return blake.hexdigest()
    
    def mine_block(self, target_difficulty: str):
        while self.hash[:len(target_difficulty)] != target_difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        return self.hash
    
    def send(self, sender: str, receiver: str, quantity: c_longdouble):
        self.data = f"{sender}:{receiver}:{quantity}"
        return True
    
    def push_raw_data(self, raw_data:str):
        self.data = raw_data
        return True
    
    def __repr__(self):
        return f"{self.data}, {self.previous_hashs}, {self.nonce}"