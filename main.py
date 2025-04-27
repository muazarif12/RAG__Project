from src.scraper import HadithScraper
from src.processor import HadithProcessor
from src.embedding import HadithEmbedder
from src.retriever import HybridRetriever
from src.generator import HadithGenerator
from src.evaluator import RagEvaluator

def main():
    # Step 1: Scrape hadith data
    scraper = HadithScraper()
    scraper.scrape_all_urls()
    
    # Step 2: Process hadith texts
    processor = HadithProcessor()
    documents = processor.process_hadiths()
    
    # Step 3: Create embeddings
    embedder = HadithEmbedder()
    vector_store = embedder.create_vector_store(documents)
    
    # Step 4: Initialize retriever
    texts = [doc.page_content for doc in documents]
    metadata = [doc.metadata for doc in documents]
    retriever = HybridRetriever(vector_store, texts, metadata)
    
    # Step 5: Initialize generator
    generator = HadithGenerator()
    
    # Example usage
    question = "What are the teachings regarding wudu?"
    results = retriever.retrieve(question, k=5)
    
    # Generate prompt and response
    prompt = f"""Your prompt construction logic here"""
    response = generator.generate_response(prompt)
    
    # Evaluate
    evaluation = RagEvaluator.evaluate_rag_output(
        question, response, results, embedder.embedding_model
    )
    
    print("Response:", response)
    print("Evaluation:", evaluation)

if __name__ == "__main__":
    main()