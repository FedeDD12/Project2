import pandas as pd 

dataset=pd.read_json("math_arXiv_v0.2_chunk_4.json", lines=True)
dataset.to_csv("~/Desktop/math_arXiv_v0.2_chunk_4.csv")
