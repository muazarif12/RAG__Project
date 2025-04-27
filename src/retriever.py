from rank_bm25 import BM25Okapi
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class HybridRetriever:
    def __init__(self, vector_store, texts, metadata):
        self.vector_store = vector_store
        self.texts = texts
        self.metadata = metadata
        
        # Initialize BM25
        self.tokenized_texts = [text.split() for text in texts]
        self.bm25 = BM25Okapi(self.tokenized_texts)
        
    def reciprocal_rank_fusion(self, results_bm25, results_embedding, k=2):
        scores = {}
        # Implementation of RRF
        # Use document content or metadata as the key
        for rank, (doc, score) in enumerate(results_bm25):
            doc_id = doc.page_content  # Or use doc.metadata.get("source", "unknown") if available
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (rank+1) # (k + rank + 1)
            print("BM25", scores[doc_id])

        for rank, (doc, score) in enumerate(results_embedding):
            doc_id = doc.page_content  # Use the same identifier
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (rank+1) # (k + rank + 1)
            print("Dense", scores[doc_id])

        return sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
    def retrieve(self, query, k=3):
        # Your existing retrieval logic
        query_embedding = embedding_model.embed_query(query)
        results_embedding = vector_store.similarity_search_with_score(query, k=k)
        results_embedding = sorted(results_embedding, key=lambda x: x[1], reverse=True)

        print("============Dense Embeddings=============")
        for doc, score in results_embedding:
            print(f"page {doc.metadata.get('page','Unknown')} - Score: {score:.4f} - {doc.page_content[:100]}...")

        # Get BM25 scores for all documents and sort to get top-k results
        results_bm25 = [(idx, bm25.get_scores(query.split())[idx]) for idx in range(len(texts))]
        results_bm25 = sorted(results_bm25, key=lambda x: x[1], reverse=True)[:k]  # Keep only top-k results
        # Convert BM25 results to (Document, score) format
        results_bm25_docs = [(Document(page_content=texts[idx], metadata=metadata[idx]), score) for idx, score in results_bm25]

        print("************BM25 Results*************")
        for doc, score in results_bm25_docs:
            print(f"page {doc.metadata.get('page','Unknown')} - Score: {score:.4f} - {doc.page_content[:100]}...")

        # Create a lookup dictionary {document content -> Document object}
        doc_lookup = {doc.page_content: doc for doc, _ in results_bm25_docs}
        doc_lookup.update({doc.page_content: doc for doc, _ in results_embedding})

        # Fuse results
        fused_results = reciprocal_rank_fusion(results_bm25_docs, results_embedding)

        # Format results, ensuring document IDs are mapped back to actual Documents
        return [format_response(doc_lookup[doc_id]) for doc_id, _ in fused_results if doc_id in doc_lookup]

        #fused_results = reciprocal_rank_fusion(results_bm25, results_embedding)
        #return [(texts[idx], metadata[idx]["page"] if "page" in metadata[idx] else "Unknown") for idx, _ in fused_results]
    
        
        pass