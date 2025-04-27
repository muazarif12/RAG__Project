# 🌙 Islamic Hadith RAG System

A Retrieval-Augmented Generation system for answering questions about Islamic Hadiths from Sahih Bukhari

# 📚 Project Overview
This project implements a Retrieval-Augmented Generation (RAG) system to answer questions about Islamic Hadiths from Sahih Bukhari. By combining traditional information retrieval techniques (BM25) with modern dense vector embeddings and the Qwen2.5-3B-Instruct language model, the system provides accurate, contextually relevant answers to user queries about Islamic teachings.

# ✨ Features

- Hybrid Retrieval System: Combines BM25 and dense embeddings through reciprocal rank fusion for improved retrieval performance
- Web Scraping Module: Automatically extracts Hadith texts from sunnah.com with proper attribution
- Chunking & Processing: Intelligently splits Hadiths into manageable chunks while preserving context
- Vector Storage: Uses Chroma DB for efficient similarity search
- Self-Evaluation: Includes metrics for evaluating response faithfulness and relevance
- Lightweight LLM: Utilizes Qwen2.5-3B-Instruct, a lightweight but powerful language model

# 🛠️ Technical Architecture

<div align="center">
  <img src="./Technical Architecture.JPG" alt="Description of image" width="80%">
</div>

# 🔍 How It Works

- **Data Collection:** Hadiths are scraped from sunnah.com's Sahih Bukhari collection
- **Processing Pipeline:** Texts are chunked into semantic units and stored with appropriate metadata
- **Dual-Retrieval System:**
  - BM25 for keyword-based retrieval  
  - BGE-small embeddings for semantic search
  - Results fused using Reciprocal Rank Fusion


- **Answer Generation:** Retrieved contexts are fed to Qwen2.5-3B-Instruct to generate comprehensive answers
- **Quality Assessment:** System evaluates its own outputs for faithfulness to retrieved documents and relevance to user queries

# 🔧 Technical Details

**Components**

- **Web Scraping:** BeautifulSoup4, requests
- **Vector Database:** ChromaDB
- **Embedding Models:** BGE-small-en
- **Language Model:** Qwen/Qwen2.5-3B-Instruct
- **Retrieval Algorithms:** BM25Okapi, FAISS similarity search, Reciprocal Rank Fusion

# Hybrid Retrieval

The system combines the strengths of sparse retrieval (BM25) and dense retrieval (vector embeddings):

- **BM25:** Excels at keyword matching and rare term retrieval
- **Vector Embeddings:** Better at semantic understanding and handling synonyms
- **Reciprocal Rank Fusion:** Combines results from both methods, giving higher weight to documents ranked highly by either system

