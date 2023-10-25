"""
This module implement Directed Acyclic Graph structure with method helps sending data
"""
import random
import json
from collections import OrderedDict
from ctypes import c_longdouble

from dream.block import Block

class DAG:
    """Implement Directed Acyclic Graph structure"""
    def __init__(self, key) -> None:
        self.graph = self.reset_graph(key)

    @staticmethod
    def reset_graph(key) -> OrderedDict:
        """This method recreate graph with geensis block"""
        graph = OrderedDict()
        block = Block([''])
        block._push("Genesis Block", key)
        graph[block.hash] = block
        return graph

    def send(self, sender: str, receiver: str, quantity: c_longdouble, privkey) -> str:
        """This function 'send' some DRM currency to receiver"""

        block = Block(
            list(dict.fromkeys(self.__choose_leaves())),
            )

        if block.hash in self.graph.keys():
            raise KeyError(f"node {block.hash} already exists")
        
        block.__push(f"{sender}:{receiver}:{quantity}", privkey)

        self.graph[block.hash] = block
        return block.hash

    def push_raw_data(self, data: str, privkey: str) -> str:
        """This function 'send' some DRM currency to receiver"""

        block = Block(
            list(dict.fromkeys(self.__choose_leaves())),
            )

        if block.hash in self.graph.keys():
            raise KeyError(f"node {block.hash} already exists")
        
        block.__push(data, privkey)

        self.graph[block.hash] = block
        return block.hash

    def all_leaves(self) -> list[str]:
        """ Return a list of all leaves (nodes with no downstreams) """
        return [key for key in self.graph if not self.graph[key]]

    def to_json(self) -> str:
        """Export DAG structure to json"""
        return json.dump(self.graph)

    def from_json(self, json_dag: str) -> bool:
        """Import DAG structure to json"""
        self.graph = OrderedDict()
        self.graph = json.loads(json_dag)
        return True

    def block(self, block_hash: str) -> Block:
        """This method helps you get Block object, when you only know a hash"""
        return self.graph[block_hash]
    
    def is_block_valid(self, block: Block):
        """Check is block valid"""
        if block.is_sign_valid():
            return True
        return False

    def size(self) -> int:
        """This method count a lenght of the graph object"""
        return len(self.graph)

    def __choose_leaves(self) -> list:
        hashs = []
        for i in self.graph.keys():
            hashs.append(i)
        k = random.randint(1,len(hashs))
        return random.choices(hashs, k=k)
