import os
import random

def load_documents(data_dir):
  documents = []
  for filename in os.listdir(data_dir):
    if filename.endswith('.txt'):
      curr_path = os.path.join(data_dir, filename)
      with open(curr_path, "r", encoding="utf-8") as f:
        content = f.read()
      documents.append({'content': content, 'source': filename})
  return documents

def chunk_documents(documents):
  chunks = []
  for i in range(len(documents)):
    content, source = documents[i].get('content'), documents[i].get('source')
    paragraphs = content.split('---')
    for paragraph in paragraphs:
      paragraph = paragraph.strip()
      if not paragraph:
        continue
      if len(paragraph) < 800:
        chunks.append({'content': paragraph, 'source': source})
      else:
        start = 0
        while start < len(paragraph):
          sliced_chunk = paragraph[start: start + 800]
          start += 700
          chunks.append({'content': sliced_chunk, 'source': source})
  return chunks
    


if __name__ == "__main__":
  documents = load_documents("data/")
  print(f"Number of documents loaded: {len(documents)}")
  for i in range(len(documents)):
    print(f"{documents[i].get('source')}")
  chunks = chunk_documents(documents)
  print(f"Total chunks: {len(chunks)}")
  for i in range(5):
    print(f"Chunk {i + 1}: {random.choice(chunks)}")
  