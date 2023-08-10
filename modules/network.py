import fastapi as _fastapi
from block import Block
from dag import DAG
from ctypes import c_longdouble

dag = DAG()
app = _fastapi.FastAPI()

@app.post("/send/")
def send(sender:str, receiver:str, quantity:c_longdouble):
    v = Block()
    v.send(sender, receiver, quantity)
    v.mine_block()
    dag.add_block(v)
    return v