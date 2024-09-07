import pandas as pd 
import os
from together import Together
import csv

dataset=pd.read_json("math_arXiv_v0.2_chunk_4.jsonl")
dataset=dataset.to_dict()
qa_pairs=[]

with open('questions_and_answers.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Question', 'Answer'])

client = Together(api_key=os.environ.get('TOGETHER_API_KEY'))

for i, text in enumerate(dataset["text"].values()):
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        messages=[ 'Generate me only one question and answer pair about the content of the following article "{}".\
          The response must be in the following format:\
          "Question: <question text>\
          Answer: <answer text>"\
          I want only questions and answers about topology.\ 
          If the article is not about topology do not generate anything.\
          Do not add an additional newline between the question and the answer.\
          Do not add any additional text other than the question and answer, do not offer other information.\
          The question must not be about mathematicians\' life.\
          If the article is about a mathematicians\' life do not generate anything.\
          The question must be a mathematical fact.\
          The answer must be as complete as possible and correlated by an explaination.\
          Do not give questions and answers about books. If the article is only about a book do not write anything.\
          Do not give answers that are too simple.\
          In the answer do not add any newline.\
          Write the answer in only one line.\
          Do not generate any list. \
          Assume that the person reading the question and answer has no access to the article and has no prior knowledge of the top],
        max_tokens=512,
        temperature=0.7,
        top_p=0.7,
        top_k=50,
        repetition_penalty=1,
        stop=["<|eot_id|>","<|eom_id|>"],
        stream=True
    )
    print(response.choices[0].message.content)

    qa_text = response.choices[0].message.content

  try:
    question, answer = qa_text.split('Answer:')

    question=question.replace("Question:", "")
  except Exception as e:
    print("Error {} encountered...skipping...".format(e))
    continue
    
  # Append the question and answer to the list as a tuple

  qa_pairs.append((question.strip(), answer.strip()))

  # Write the question-answer pairs to a CSV file
  with open('questions_and_answers.csv', 'a', newline='', encoding='utf-8') as file:
      writer = csv.writer(file)
      writer.writerow(qa_pairs[-1])  # Write the question-answer pairs
