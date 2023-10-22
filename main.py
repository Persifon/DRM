from dream.dag import DAG
from dream.block import Block
from dream.crypto import key_pair_gen

with open("privkey.bin", "wb") as f:
    f.write(key_pair_gen()[1])

dag = DAG()
block = Block()

BLOCK_IN_DAG = dag.send("Alice", "Bob", 12.1, block)
print(dag.is_block_valid(dag.graph[BLOCK_IN_DAG]))

print(dag.graph)
