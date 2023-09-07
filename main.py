from modules.dag import DAG
from modules.block import Block

d = DAG()
v = Block()

b = d.send("Alice", "Bob", 12.1, v)

print(d.graph)