
from langchain_core.embeddings import Embeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from typing import List
import os


class ChromaDB:                              

    def __init__(self, embedder: Embeddings):
        self.embedder = embedder
        self.persist_directory = "db/Chroma_db"
        self.vectorstore = None

    def create_index(self) -> None:
        if os.path.exists(self.persist_directory):
            print("Index already exists")
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedder
            )
        else:
            print("No index found")

    def upload_documents(self, folder_path: str) -> None:
        all_chunks = []
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1250,
            chunk_overlap=250
        )

        for file in os.listdir(folder_path):
            if file.endswith(".pdf"):
                print(f"Processing {file}...")
                loader = PyPDFLoader(os.path.join(folder_path, file))
                pages = loader.load()
                chunks = splitter.split_documents(pages)
                all_chunks.extend(chunks)

        print(f"Total chunks: {len(all_chunks)}")

        self.vectorstore = Chroma.from_documents(
            documents=all_chunks,
            embedding=self.embedder,
            persist_directory=self.persist_directory,
            collection_metadata={"hnsw:space": "cosine"}
        )
        print("Upload complete!")

    def search(self, query: str, top_k: int = 5) -> List[str]:
        results = self.vectorstore.similarity_search(query, k=top_k)
        return [doc.page_content for doc in results]


