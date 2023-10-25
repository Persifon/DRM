import fastapi as _fastapi
from dag import DAG
from ctypes import c_longdouble
import random

dag = DAG()
app = _fastapi.FastAPI()

@app.post("/send/")
def send(sender:str, receiver:str, quantity:c_longdouble, privkey: str):
    return dag.send(sender, receiver, quantity, privkey)

@app.post("/mine/")
def mine():
    leaves = list(dict.fromkeys(dag.__choose_leaves()))
    
    not_mined_blocks = []
    for _, val in enumerate(leaves):
        if dag[val] == "":
            not_mined_blocks.append(val)
    mine_block = random.choice(not_mined_blocks)
    dag[mine_block].mine()