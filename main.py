from modules import dag, block

Block = block.Block()

Dag = dag.DAG()

Block.push_raw_data("абракадабра")
Dag.add_block(Block)