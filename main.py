from dream.dag import DAG
from dream.crypto import key_pair_gen

with open("privkey.bin", "wb") as f:
    key = key_pair_gen()
    f.write(key['sk'])

dag = DAG(key)

BLOCK_IN_DAG = dag.send("Alice", "Bob", 12.1, key)
print(dag.is_block_valid(dag.graph[BLOCK_IN_DAG], key))

print(dag.graph)
