from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from tqdm import tqdm
import os

class HadithProcessor:
    def __init__(self, data_folder="data/hadith_texts"):
        self.data_folder = data_folder
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
            add_start_index=True
        )

    def process_hadiths(self):
        documents = []
        hadith_files = [f for f in os.listdir(self.data_folder) if f.endswith("_english.txt")]
        
        for file_name in tqdm(hadith_files, desc="Processing files"):
            try:
                file_path = os.path.join(self.data_folder, file_name)
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read().strip()
                
                hadiths = [h.strip() for h in content.split('='*50) if h.strip()]
                
                for hadith_num, hadith_text in enumerate(hadiths, 1):
                    doc = Document(
                        page_content=hadith_text,
                        metadata={
                            "source": file_name,
                            "hadith_num": hadith_num,
                            "is_chunked": False
                        }
                    )
                    hadith_chunks = self.text_splitter.split_documents([doc])
                    
                    for chunk_num, chunk in enumerate(hadith_chunks, 1):
                        chunk.metadata.update({
                            "is_chunked": len(hadith_chunks) > 1,
                            "chunk_num": chunk_num if len(hadith_chunks) > 1 else 0,
                            "total_chunks": len(hadith_chunks) if len(hadith_chunks) > 1 else 1
                        })
                    
                    documents.extend(hadith_chunks)
                    
            except Exception as e:
                print(f"Error processing {file_name}: {str(e)}")
                continue
                
        return documents