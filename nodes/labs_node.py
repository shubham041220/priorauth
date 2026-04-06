import os
import json
from agents.json_extractor_agent import extract_json_usingprompt
from models.labs_mode import LabsData 

def labs_node(state, llm,ocr):

    schema = LabsData.model_json_schema()
    prompt = f"""
    You are extracting structured laboratory results
    from a medical document.

    Mark each result as HIGH, LOW, NORMAL or ABNORMAL where applicable.

    Return JSON matching this exact schema:
    {json.dumps(schema, indent=2)}

    If any field is missing return null.
    Do not return explanations.
    Return only valid JSON.
    """

    print("Current State in LABS Node: ", state)

    text = ocr.ocr("inputpdf/labs.pdf")

    raw_output = extract_json_usingprompt(text, prompt, llm)  
    try:
        labs_data = LabsData(**raw_output)
    except Exception as e:
        print(f"Pydantic validation failed: {e}")
        labs_data = LabsData()
   

    os.makedirs("output", exist_ok=True)

    with open("output/labs.json", "w") as f:
        json.dump(labs_data.model_dump(), f, indent=4) 


    return {"labs_data": labs_data.model_dump()} 
