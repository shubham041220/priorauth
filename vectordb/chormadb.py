
from langchain_core.embeddings import Embeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import CrossEncoderReranker
import pickle

from typing import List
import os


class ChromaDB:                              

    def __init__(self, embedder: Embeddings):
        self.embedder = embedder
        self.persist_directory = "db/Chroma_db"
        self.vectorstore = None
        self.all_chunks=[]

    def create_index(self) -> None:
        if os.path.exists(self.persist_directory):
            print("Index already exists")
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedder
            )
            if os.path.exists("db/chunks.pkl"):
                with open("db/chunks.pkl", "rb") as f:
                 self.all_chunks = pickle.load(f)
        else:
            print("No index found")

    def upload_documents(self, folder_path: str) -> None:
        all_chunks = []
        os.makedirs("db", exist_ok=True)

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
        self.all_chunks=all_chunks
        with open("db/chunks.pkl", "wb") as f:
            pickle.dump(all_chunks, f)

        print(f"Total chunks: {len(all_chunks)}")

        self.vectorstore = Chroma.from_documents(
            documents=all_chunks,
            embedding=self.embedder,
            persist_directory=self.persist_directory,
            collection_metadata={"hnsw:space": "cosine"}
        )
        print("Upload complete!")

    def search(self, query: str, top_k: int = 5) -> List[str]:
        vector_retriever = self.vectorstore.as_retriever(
        search_kwargs={"k": top_k}
    )

        bm25_result=BM25Retriever.from_documents(self.all_chunks)
        bm25_result.k=top_k

        ensemble_retriever=EnsembleRetriever(
            retrievers=[vector_retriever, bm25_result],
            weights=[0.6, 0.4]
            
        )

        reranker_model=HuggingFaceCrossEncoder(
            model_name="cross-encoder/ms-marco-MiniLM-L-6-v2" 
        )
        reranker=CrossEncoderReranker(model=reranker_model, top_n=3)

        compression_retriever=ContextualCompressionRetriever(
            base_compressor=reranker,
            base_retriever=ensemble_retriever
        )
        results=compression_retriever.invoke(query)
        return [doc.page_content for doc in results]


