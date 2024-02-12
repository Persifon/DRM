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

    def __init__(self) -> None:
        self.graph = OrderedDict()

    def send(self, sender: str, receiver: str, quantity: c_longdouble, key: dict[str, bytes]) -> str:
        """This function 'send' some DRM currency to receiver"""

        block = Block(
            list(dict.fromkeys(self.__choose_leaves())),
        )
        block._push(f"{sender}:{receiver}:{quantity}", key)
        if block.hash in self.graph.keys():
            raise KeyError(f"Block {block.hash} already in DAG")
        self.graph[block.hash] = block

        return block.hash

    def genesis_block(self, key: dict[str, bytes]):
        """Generate genesis block"""

        block = Block([])
        block._push('Genesis block', key)
        self.graph[block.hash] = block

        return block.hash

    def push_raw_data(self, data: str, key: dict[str, bytes]) -> str:
        """This function 'send' some DRM currency to receiver"""

        block = Block(
            list(dict.fromkeys(self.__choose_leaves())),
        )
        block._push(data, key)
        if block.hash in self.graph.keys():
            raise KeyError(f"Block {block.hash} already in DAG")
        self.graph[block.hash] = block

        return block.hash.decode('utf-8')

    def all_leaves(self) -> list[str]:
        """Return a list of all leaves (nodes with no downstreams)"""
        
        leaves = [key for key in self.graph if not self.graph[key]]

        return leaves

    def to_json(self) -> str:
        """Export DAG structure to json"""
        
        return json.dump(self.graph)

    def from_json(self, json_dag: str) -> bool:
        """Import DAG structure from json"""

        self.graph = OrderedDict()
        self.graph = json.loads(json_dag)
        
        return True

    def get_block(self, block_hash: str) -> Block:
        """This method helps you get Block object, when you only know a hash"""
        
        return self.graph[block_hash.encode()]

    def is_block_valid(self, block: Block):
        """Check is block valid"""

        return block._is_sign_valid()

    def size(self) -> int:
        """This method count lenght of the graph object"""

        return len(self.graph)

    def __choose_leaves(self) -> list:
        """This method choose leaves"""
        
        hashs = []
        for i in self.graph.keys():
            hashs.append(i)
        k = random.randint(1, len(hashs))
        
        return random.choices(hashs, k=k)
