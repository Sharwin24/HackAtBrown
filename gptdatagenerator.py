import numpy as np
import torch
import openai

with open('/home/iyer.ris/key.txt', 'r') as file:
  openai.api_key = file.read().rstrip()

with open('/home/iyer.ris/graphcast/graphcast/solar_radiation.py', 'r') as file:
  file_content=file.read()
response = openai.Completion.create(
  model="gpt-4",
  prompt="This is a Python file content: {}\n\nPlease generate 2 questions regarding this code, along with 2 answers to the questions".format(file_content),
  max_tokens=200
)

print(response.choices[0].text.strip())
