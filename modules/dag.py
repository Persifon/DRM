from pgmpy.base import DAG as d
from block import Block
import random

# TODO: скорее всего полностью с нуля перепишу на golang, так как не хочу зависеть от разраба pgmpy
class DAG:
    def __init__(self) -> None:
        self.dag: d = d()
        self.genesis_block = self._create_genesis_block()
        self.dag.add_node(node=self.genesis_block)
        self.previous_blocks: list[Block] = [self.genesis_block]


    def add_block(self, new_block: Block):
        leaves = self.dag.get_leaves() 
        if self.previous_blocks not in leaves:
            leaves.append(self.previous_blocks)
        leaves = list(dict.fromkeys(leaves))
        edge_blocks = list(dict.fromkeys(self._choose_leaves(leaves)))
        new_block.previous_hashs = ",".join(self._get_hashs(edge_blocks))
        print(new_block.previous_hashs)
        for i in edge_blocks:
            self.dag.add_edge(u=i, v=new_block)
        self.previous_blocks = edge_blocks

        if new_block in self.dag:
            return True
        else:
            False


    def _create_genesis_block(self):
        gen = Block()
        gen.push_raw_data("Genesis Block")
        return gen


    def _choose_leaves(self, leaves: list):
        k = random.randint(1,len(leaves))
        self.dag.update
        return random.choices(leaves, k=k)


    def _get_hashs(self, leaves: list[Block]) -> list:
        hashs = []
        for i in leaves:
            hashs.append(i.hash)
        return hashs


    def get_leaves(self) -> list[Block]:
        return self.dag.get_leaves()


    def get_difficulty(self) -> str:
        default = "0"*64
        
        return ""