import os
import collections
from retrieve import retrieve
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def generate(query):
  top_five_chunks = retrieve(query)
  chunk = collections.defaultdict(str)
  for i in range(5):
    chunk[f"source"] += top_five_chunks['metadatas'][0][i]['source'] + "\n"
    chunk[f"context"] += top_five_chunks['documents'][0][i] + "\n\n"
  res = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "Answer the question using only the information in the provided documents. If the documents don't contain enough information to answer, say 'I don't have enough information on that.'"},
        {"role": "user", "content": f"Context:\n{chunk.get('context')}\n\nQuestion: {query}"}
    ]
  )   
  return res.choices[0].message.content, chunk.get('source')

if __name__ == "__main__":
  print(generate('What do students say about CS111\'s difficulty and how should a complete beginner prepare?'))
  print(generate('What are the most common complaints about Professor Francisco in CS214 and is it worth taking with him?'))
  print(generate('What are the easiest SAS core courses to fulfill writing and humanities requirements at Rutgers?'))