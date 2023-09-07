import random
import json
from collections import OrderedDict
from ctypes import c_longdouble

from modules.block import Block

class DAGValidationError(Exception):
    pass

class DAG:
    def __init__(self) -> None:
        self.graph = OrderedDict()
        b = Block()
        b.data = "Genesis Block"
        b.calculate_hash()
        self.graph["Genesis Block"] = b
    
    def reset_graph(self) -> OrderedDict:
        self.graph = OrderedDict()
        return self.graph
    
    def send(self, sender: str, receiver: str, quantity: c_longdouble, block: Block) -> str:

        if block.hash in self.graph.keys():
            raise KeyError('node %s already exists' % block.hash)
        
        block.data = f"{sender}:{receiver}:{quantity}"
        leaves = self.all_leaves()

        leaves = list(dict.fromkeys(leaves))
        block.previous_hashs = list(dict.fromkeys(self.__choose_leaves(leaves)))
        block.hash = block.calculate_hash()

        self.graph[block.hash] = block
        return block.hash
    
    def push_raw_data(self, data: str, block: Block) -> str:

        if block.hash in self.graph.keys():
            raise KeyError('node %s already exists' % block.hash)
        
        block.data = data
        leaves = self.all_leaves()

        leaves = list(dict.fromkeys(leaves))
        block.previous_hashs = list(dict.fromkeys(self.__choose_leaves(leaves)))
        block.hash = block.calculate_hash()

        self.graph[block.hash] = block
        return block.hash
        

    def all_leaves(self) -> list[str]:
        """ Return a list of all leaves (nodes with no downstreams) """
        return [key for key in self.graph if not self.graph[key]]

    #TODO Надо сделать jsonization и dejsonization
    def to_json(self) -> str:
        return json.dump(self.graph)
    
    def from_json(self, json_dag: str) -> bool:
        self.reset_graph()
        self.graph = json.loads(json_dag)
        return True
    
    def block(self, hash: str) -> Block:
        return self.graph[hash]

    def size(self) -> int:
        return len(self.graph)

    def __choose_leaves(self, leaves: list[str]) -> list:
        hashs = []
        for i in self.graph.keys():
            hashs.append(i)
        k = random.randint(1,len(hashs))
        return random.choices(hashs, k=k)