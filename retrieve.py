import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="db")
collection = client.get_or_create_collection(name="rutgers_guide")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve(query):
  embedded_query = embedding_model.encode(query)
  results = collection.query(
    query_embeddings=[embedded_query],
    n_results=5,
    include=['documents','metadatas','distances']
  )
  return results

if __name__ == "__main__":
  print(retrieve('What do students say about CS111\'s difficulty and how should a complete beginner prepare?'))
  print(retrieve('What are the most common complaints about Professor Francisco in CS214?'))
  print(retrieve('"What study strategies do Rutgers students recommend for passing Calc 2?'))