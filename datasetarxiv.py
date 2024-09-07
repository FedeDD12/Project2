import pandas as pd 

dataset=pd.read_csv("math_arXiv_v0.2_chunk_4.csv")
print(dataset)
import os
from together import Together

client = Together(api_key=os.environ.get('TOGETHER_API_KEY'))

response = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    messages=[],
    max_tokens=512,
    temperature=0.7,
    top_p=0.7,
    top_k=50,
    repetition_penalty=1,
    stop=["<|eot_id|>","<|eom_id|>"],
    stream=True
)
print(response.choices[0].message.content)
