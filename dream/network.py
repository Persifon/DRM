import fastapi as _fastapi
from block import Block
from dag import DAG
from ctypes import c_longdouble
import random

dag = DAG()
app = _fastapi.FastAPI()

@app.post("/send/")
def send(sender:str, receiver:str, quantity:c_longdouble):
    v = Block()
    v.send(sender, receiver, quantity)
    dag.add_block(v)
    return v

@app.post("/mine/")
def mine():
    leaves = dag.get_leaves()
    
    not_mined_blocks = []
    for ind, val in enumerate(leaves):
        if val.hash == "":
            not_mined_blocks.append(val)
    mine_block = random.choice(not_mined_blocks)
    mine_block.mine_block()