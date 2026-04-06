import os
import json
from agents.json_extractor_agent import extract_json_usingprompt
from llm.mistral import LLMClient
from models.form_model import FormData 
from ocr.ocr_space import OCRSpaceClient

def form_node(state, llm,ocr):

    schema = FormData.model_json_schema()
    prompt = f"""
    You are extracting structured demographic and provider information
    from a prior authorization form.

    Return JSON matching this exact schema:
    {json.dumps(schema, indent=2)}

    If any field is missing return null.
    Do not return explanations.
    Return only valid JSON.
    """

    print("Current State in Form Node: ", state)

    text = ocr.ocr("inputpdf/form.pdf")

    raw_output = extract_json_usingprompt(text, prompt, llm)  
    try:
        form_data = FormData(**raw_output)
    except Exception as e:
        print(f"Pydantic validation failed: {e}")
        form_data = FormData()
   

    form_data = FormData(**raw_output)

    os.makedirs("output", exist_ok=True)

    with open("output/form.json", "w") as f:
        json.dump(form_data.model_dump(), f, indent=4) 


    return {"form_data": form_data.model_dump()} 
