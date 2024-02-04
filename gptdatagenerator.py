import numpy as np
from openai import OpenAI
import os
import json
from model import Embedder

class QAGenerator:
  def __init__(self, json_path="./"):
    os.environ['OPENAI_API_KEY'] = self.read_key()
    self.client = OpenAI()
    self.qa = {}
    
    self.generate_qa_from_json(json_path)
    
    self.embedded_questions = self.embed_questions()
    self.embedded_answers = self.embed_answers()

    self.save_embeddings("questions.npy", "answers.npy")
  
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
      model="gpt-3.5-turbo",
      messages=messages,
    )

    json_response = response.choices[0].message.content

    try:
      qa = json.loads(json_response)
    except:
      return "Error parsing response"
    
    return qa

  def embed_questions(self):
    questions = [q['question'] for qa in self.qa for q in qa]
    embedder = Embedder("microsoft/codebert-base")
    return embedder.embed(questions)

  def embed_answers(self):
    answers = [q['answer'] for qa in self.qa for q in qa]
    embedder = Embedder("microsoft/codebert-base")
    return embedder.embed(answers)
  
  def save_embeddings(self, file_q_path, file_a_path):
    with open(file_q_path, 'wb') as file_q:
      np.save(file, self.embedded_questions)
    
    with open(file_a_path, 'wb') as file_a:
      np.save(file, self.embedded_answers)
    
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
  
  def generate_qa_from_json(self, json_path):
    with open(json_path, 'r') as file:
      data = json.load(file)
      for node, code in data.items():
        self.qa[node] = self.generate_qa(code)
      
if __name__ == "__main__":
  json_path = "./example_codebase.json"
  qa_generator = QAGenerator(json_path)

  qa_json = "./qa.json"
  with open(qa_json, 'w') as file:
    json.dump(qa_generator.qa, file)
