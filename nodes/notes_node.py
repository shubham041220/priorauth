import os
import json
from agents.json_extractor_agent import extract_json_usingprompt
from models.notes_model import NotesData 

def notes_node(state, llm,ocr):

    schema = NotesData.model_json_schema()

    prompt = f"""
    You are extracting clinical narrative information
    from a physician's notes for a prior authorization case.

    If an ICD-10 code is not explicitly present but diagnosis is clear,
    infer the most appropriate ICD-10 code.
    If uncertain return null.

    Return JSON matching this exact schema:
    {json.dumps(schema, indent=2)}

    If any field is missing return null.
    Do not return explanations.
    Return only valid JSON.
    """

    print("Current State in notes Node: ", state)

    text = ocr.ocr("inputpdf/notes.pdf")

    raw_output = extract_json_usingprompt(text, prompt, llm)  
    try:
        notes_data = NotesData(**raw_output)
    except Exception as e:
        print(f"Pydantic validation failed: {e}")
        notes_data = NotesData()
   

    os.makedirs("output", exist_ok=True)

    with open("output/notes.json", "w") as f:
        json.dump(notes_data.model_dump(), f, indent=4) 


    return {"notes_data": notes_data.model_dump()} 
