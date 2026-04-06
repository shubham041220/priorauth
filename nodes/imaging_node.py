import os
import json
from agents.json_extractor_agent import extract_json_usingprompt
from models.imaging_model import ImagingData 


def imaging_node(state, llm,ocr):

    schema = ImagingData.model_json_schema()
    prompt = f"""
    You are extracting structured demographic and provider information
    from a prior authorization form.

    Return JSON matching this exact schema:
    {json.dumps(schema, indent=2)}

    If any field is missing return null.
    Do not return explanations.
    Return only valid JSON.
    """

    print("Current State in Imaging Node: ", state)

    text = ocr.ocr("inputpdf/imaging.pdf")

    raw_output = extract_json_usingprompt(text, prompt, llm)  
    try:
        imaging_data = ImagingData(**raw_output)
    except Exception as e:
        print(f"Pydantic validation failed: {e}")
        imaging_data = ImagingData()
   

    os.makedirs("output", exist_ok=True)

    with open("output/imaging.json", "w") as f:
        json.dump(imaging_data.model_dump(), f, indent=4) 


    return {"imaging_data": imaging_data.model_dump()} 
