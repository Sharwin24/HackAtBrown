import numpy as np
import torch
from openai import OpenAI
import os
import json
from model import Embedder

class QAGenerator:
  def __init__(self, dir_path="./"):
    os.environ['OPENAI_API_KEY'] = self.read_key()
    self.client = OpenAI()
    self.qa = self.generate_qa_from_directory(dir_path)
    
    self.embedded_questions = self.embed_questions()
    self.embedded_answers = self.embed_answers()
  
  def read_key(self, key_path="./key.txt"):
    with open(key_path, 'r') as file:
      return file.read().rstrip()
  
  def generate_qa(self, file_content):
    messages=[
      {
        "role": "user",
        "content": f"Given the following code, generate two question and answer pairs",
      },
      {"role": "user", 
       "content": f"Here is the code :\n\n{file_content}",
      },
      {
        "role": "user",
        "content": f"It is EXTREMELY IMPORTANT to format like a list of Python dicts with each with a question key and value given by the generated question string, and a answer key with the values being the generated answer string so that it is JSON parseable",
      }, 
    ]

    if len(file_content) > 4096:
      return "Code too long to process"

    response = self.client.chat.completions.create(
      model="gpt-3.5",
      messages=messages,
      response_format={"type": "json_object"}
    )

    json_response = response.choices[0].message.content
    print(json_response)
    qa = json.loads(json_response)
    return qa

  def embed_questions(self):
    questions = [q['question'] for qa in self.qa for q in qa]
    embedder = Embedder("microsoft/codebert-base")
    return embedder.embed(questions)

  def embed_answers(self):
    answers = [q['answer'] for qa in self.qa for q in qa]
    embedder = Embedder("microsoft/codebert-base")
    return embedder.embed(answers)
    
  def generate_qa_from_file(self, file_path):
    with open(file_path, 'r') as file:
      file_content = file.read()
      return self.generate_qa(file_content)
  
  def generate_qa_from_files(self, file_paths):
    file_qa = {}
    for file_path in file_paths:
      file_qa[file_path] = self.generate_qa_from_file(file_path)
    return file_qa
  
  def generate_qa_from_directory(self, directory_path):
    file_paths = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith('.py')]
    return self.generate_qa_from_files(file_paths)
  
if __name__ == "__main__":
  dir_path = '/Users/arnavb/Code/projects/graphcast/graphcast/'
  qa_generator = QAGenerator(dir_path)

  print(qa_generator.qa)