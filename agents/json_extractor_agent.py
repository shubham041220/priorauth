import json

def extract_json_usingprompt(text: str, sysprompt: str, llm) -> dict:

    system_message = "You extract structured JSON from documents."
    human_message = f"{sysprompt}\n\nDocument:\n{text}"

    response_text = llm.chat(system_message, human_message)

    if isinstance(response_text, list):
        response_text = response_text[0]

    return json.loads(response_text)