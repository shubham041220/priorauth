import os
CHROMA_DB_PATH = "db/Chroma_db"

def orchestrator_node(state,vectordb):

    print("\nOrchestrator: Checking index...")

    if os.path.exists(CHROMA_DB_PATH):
        print("Index exists → skipping indexing")
        vectordb.create_index()             # ← load it here!

        return {"index_ready": True}

    print("Index NOT found → need to create")
    return {"index_ready": False}