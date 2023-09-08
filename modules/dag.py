"""
This module implement Directed Acyclic Graph structure with method helps sending data
"""
import random
import json
from collections import OrderedDict
from ctypes import c_longdouble

from modules.block import Block

class DAG:
    """Implement Directed Acyclic Graph structure"""
    def __init__(self) -> None:
        self.graph = self.reset_graph()

    @staticmethod
    def reset_graph() -> OrderedDict:
        """This method recreate graph with geensis block"""
        graph = OrderedDict()
        block = Block()
        block.data = "Genesis Block"
        block.calculate_hash()
        graph["Genesis Block"] = block
        return graph

    def send(self, sender: str, receiver: str, quantity: c_longdouble, block: Block) -> str:
        """This function 'send' some DRM currency to receiver"""
        if block.hash in self.graph.keys():
            raise KeyError(f"node {block.hash} already exists")

        block.data = f"{sender}:{receiver}:{quantity}"
        leaves = self.all_leaves()

        leaves = list(dict.fromkeys(leaves))
        block.previous_hashs = list(dict.fromkeys(self.__choose_leaves(leaves)))
        block.hash = block.calculate_hash()

        self.graph[block.hash] = block
        return block.hash

    def push_raw_data(self, data: str, block: Block) -> str:
        """This function push raw string data to BlockDAG"""
        if block.hash in self.graph.keys():
            raise KeyError(f"node {block.hash} already exists")

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

    def size(self) -> int:
        """This method count a lenght of the graph object"""
        return len(self.graph)

    def __choose_leaves(self, leaves: list[str]) -> list:
        hashs = []
        for i in self.graph.keys():
            hashs.append(i)
        k = random.randint(1,len(hashs))
        return random.choices(hashs, k=k)