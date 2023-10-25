from dream.dag import DAG
from dream.block import Block
from dream.crypto import key_pair_gen

with open("privkey.bin", "wb") as f:
    key = key_pair_gen()

dag = DAG(key)

BLOCK_IN_DAG = dag.send("Alice", "Bob", 12.1, key)
print(dag.is_block_valid(dag.graph[BLOCK_IN_DAG]))

print(dag.graph)
