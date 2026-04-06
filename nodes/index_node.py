import os
def index_node(state, vectordb):
    vectordb.create_index()          
    if not os.path.exists("db/Chroma_db"):
        vectordb.upload_documents("policies/")   
    return {"index_ready": True}