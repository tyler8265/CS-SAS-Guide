from ingest import load_documents, chunk_documents
from sentence_transformers import SentenceTransformer
import chromadb

client = chromadb.PersistentClient(path="db")
collection = client.get_or_create_collection(name="rutgers_guide")

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

if __name__ == "__main__":
  documents = load_documents('data/')
  chunks = chunk_documents(documents)
  embedding = []
  for i in range(len(chunks)):
    embedding.append(embedding_model.encode(chunks[i].get('content')))
    collection.add(
      ids=[f"chunk_{i}"],
      documents=[chunks[i].get('content')],
      embeddings=[embedding[i]],
      metadatas=[{'source': chunks[i].get('source')}]
    )