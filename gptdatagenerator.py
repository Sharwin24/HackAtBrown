import numpy as np
import torch
from openai import OpenAI
import os

class QAGenerator:
  def __init__(self):
    os.environ['OPENAI_API_KEY'] = self.read_key()
    self.client = OpenAI()
  
  def read_key(self, key_path="./key.txt"):
    with open(key_path, 'r') as file:
      return file.read().rstrip()
  
  def generate_qa(self, file_content):
    message=[
      {"role": "assistant", 
       "content": f"Your task is to generate two question and answer pairs for the following code:\n\n{file_content}"
      }, 
    ]

    response = self.client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=message,
    )
    
    return response.choices[0].text.strip()
  
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
  qa_generator = QAGenerator()

  dir_path = '/Users/arnavb/Code/projects/graphcast/graphcast/'
  print(qa_generator.generate_qa_from_directory(dir_path))