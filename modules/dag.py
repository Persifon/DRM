from pgmpy.base import DAG as d
from block import Block
import random

class DAG:
    def __init__(self) -> None:
        self.dag = d()
        self.genesis_block = self.create_genesis_block()
        self.dag.add_node(node=self.genesis_block)
        self.previous_block = self.genesis_block
    
    def add_block(self, new_block: Block):
        leaves = self.dag.get_leaves() 
        if self.previous_block not in leaves:
            leaves.append(self.previous_block)
        leaves = list(dict.fromkeys(leaves))
        edge_blocks = list(dict.fromkeys(self.choose_leaves(leaves)))
        new_block.previous_hashs = ",".join(self.get_hashs(edge_blocks))
        print(new_block.previous_hashs)
        new_block.hash = new_block.mine_block('0000')
        print(f"Block {new_block.data} mined: {new_block.hash}")
        for i in edge_blocks:
            self.dag.add_edge(u=i, v=new_block)
        self.previous_block = random.choice(edge_blocks)
        
        if new_block in self.dag:
            return True
        else:
            False
    
    def create_genesis_block(self):
        gen = Block()
        gen.push_raw_data("Genesis Block")
        gen.mine_block("0")
        return gen
    
    def choose_leaves(self, leaves: list):
        k = random.randint(1,len(leaves))
        return random.choices(leaves, k=k)
    
    def get_hashs(self, leaves: list[Block]) -> list:
        hashs = []
        for i in leaves:
            hashs.append(i.hash)
        return hashs