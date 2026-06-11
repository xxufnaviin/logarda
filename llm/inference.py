# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

messages = [
    {"role": "user", "content": "Who are you?"},
]

response = pipe(messages, max_new_tokens = 20)
response = response[0]["generated_text"][1]["content"]

text = input(response)

messages = [
    {"role": "user", "content": text},
]
response = pipe(messages, max_new_tokens = 20)
print(response[0]["generated_text"][1]["content"])