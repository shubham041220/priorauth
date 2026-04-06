import json
import os
from schema.masterschema import PriorAuthMasterSchema


def deep_merge(master, new_data):
    for key in new_data:
        if new_data[key] is None:
            continue

        if isinstance(master.get(key), dict) and isinstance(new_data[key], dict):
            deep_merge(master[key], new_data[key])
        else:
            master[key] = new_data[key]

    return master


def generate_lab_summary(lab_results: dict, llm) -> dict:
    if not lab_results:
        return {}

    prompt = f"""
    Interpret the following lab results and summarize key abnormalities.
    Return ONLY valid JSON in this format:
    {{
        "clinical_information": {{
            "lab_summary": "<summary>"
        }}
    }}
    Lab Results:
    {json.dumps(lab_results)}
    """

    response = llm.chat(
        "You summarize medical lab findings.",
        prompt
    )

    try:
        return json.loads(response)
    except Exception as e:
        print(f"Lab summary generation failed: {e}")
        return {}


def aggregator_node(state, llm):

    print("\nStarting aggregation...")

    # ── Start with empty master schema ────────────────────────────────
    master_dict = PriorAuthMasterSchema().model_dump()

    # ── Merge all 4 node outputs ───────────────────────────────────────
    partial_results = [
        state.get("form_data"),
        state.get("labs_data"),
        state.get("imaging_data"),
        state.get("notes_data")
    ]

    for partial in partial_results:
        if partial:
            print("Merging partial result...")
            master_dict = deep_merge(master_dict, partial)

    # ── Generate lab summary via LLM ───────────────────────────────────
    lab_results = master_dict["clinical_information"].get("lab_results")

    if lab_results:
        print("Generating lab summary via LLM...")
        summary_json = generate_lab_summary(lab_results, llm)
        master_dict = deep_merge(master_dict, summary_json)
        master_dict["clinical_information"].pop("lab_results", None)

    # ── Validate with Pydantic ─────────────────────────────────────────
    try:
        final_object = PriorAuthMasterSchema(**master_dict)
    except Exception as e:
        print(f"Pydantic validation failed: {e}")
        final_object = PriorAuthMasterSchema()

    # ── Save to file ───────────────────────────────────────────────────
    os.makedirs("output", exist_ok=True)
    with open("output/final_prior_auth.json", "w", encoding="utf-8") as f:
        json.dump(final_object.model_dump(), f, indent=4, ensure_ascii=False)

    print("Aggregation complete!")

    return {"final_prior_auth": final_object.model_dump()}