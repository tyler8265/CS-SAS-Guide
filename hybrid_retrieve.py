from ingest import load_documents, chunk_documents
from retrieve import retrieve
from rank_bm25 import BM25Okapi
from collections import defaultdict

documents = load_documents("data/")
chunks = chunk_documents(documents)
tokenized_list = []
for chunk in chunks:
  content = chunk.get('content').lower()
  tokenized_list.append(content.split(' '))
bm25 = BM25Okapi(tokenized_list)

def hybrid_retrieve(query: str) -> str:
  semantic, rrf_scores = retrieve(query), defaultdict(int)
  for rank, id in enumerate(semantic["ids"][0]):
    index = int(id.replace("chunk_", '') )
    rrf_scores[index] += 1 /(rank + 60)
  tokenized_query = query.lower().split(' ')
  scores = bm25.get_scores(tokenized_query)
  top5_bm25 = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:5]
  for rank, index in enumerate(top5_bm25):
    rrf_scores[index] += 1 / (rank + 60)
  top5 = []
  for key, val in rrf_scores.items():
    top5.append((key, val))
  top5.sort(key=lambda x: x[1], reverse=True)
  top5 = top5[:5]
  results = [chunks[index] for index, score in top5]
  return {
    "documents": [[chunk["content"] for chunk in results]],
    "metadatas": [[{"source": chunk["source"]} for chunk in results]]
  }

if __name__ == "__main__":
  print(hybrid_retrieve('What do students say about CS111\'s difficulty and how should a complete beginner prepare?'))
  print(hybrid_retrieve('What are the most common complaints about Professor Francisco in CS214?'))
  print(hybrid_retrieve('"What study strategies do Rutgers students recommend for passing Calc 2?'))


