from langchain_huggingface import HuggingFaceEmbeddings


class HFEmbeddings(HuggingFaceEmbeddings):

    def __init__(self):
        super().__init__(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},   # use "cuda" if you have GPU
            encode_kwargs={"normalize_embeddings": True}
        )