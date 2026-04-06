
import json
import os
from datetime import datetime



# ── Query Builder ──────────────────────────────────────────────────────
def build_query(final_json: dict) -> str:
    clinical = final_json.get("clinical_information", {})
    treatment = clinical.get("treatment_request", {})

    query = f"""
    Diagnosis: {clinical.get('diagnosis', '')}
    ICD: {clinical.get('icd_10_code', '')}
    Medication: {treatment.get('name_of_medication_or_procedure', '')}
    Symptoms: {clinical.get('symptom_severity_and_impact', '')}
    Prior Treatment: {clinical.get('prior_treatments_and_results', '')}
    """
    return query.strip()


# ── Policy Evaluator ───────────────────────────────────────────────────
def evaluate_policy(final_json: dict, policies: list, llm) -> dict:

    prompt = f"""
    You are a medical prior authorization decision engine.

    STRICT RULES:
    - Use ONLY the provided policy chunks
    - Do NOT assume missing data
    - If insufficient info → NEED_MORE_INFO

    Return ONLY valid JSON:
    {{
        "decision": "APPROVED / DENIED / NEED_MORE_INFO",
        "confidence": 0.0-1.0,
        "reason": "<clear explanation>",
        "policy_references": ["policy file names used"],
        "matched_policy_text": "<exact relevant snippet>"
    }}

    Patient Case:
    {json.dumps(final_json)}

    Policy Chunks:
    {json.dumps(policies)}
    """

    response = llm.chat(
        "You are a strict healthcare policy evaluator.",
        prompt
    )

    try:
        return json.loads(response)
    except Exception as e:
        print(f"Policy evaluation failed: {e}")
        return {
            "decision": "NEED_MORE_INFO",
            "confidence": 0.0,
            "reason": "Failed to parse LLM response",
            "policy_references": [],
            "matched_policy_text": ""
        }


# ── Policy Node ────────────────────────────────────────────────────────
def policy_node(state, llm, vectordb):         # ← llm and vectordb injected

    print("\nInside Policy Node")

    final_json = state.get("final_prior_auth")

    if not final_json:
        print("No final JSON found")
        return {"final_decision": None}

    # ── Build query from patient data ──────────────────────────────────
    query = build_query(final_json)
    policies = vectordb.search(query, top_k=5)

    decision = evaluate_policy(final_json, policies, llm)  # ← uses injected llm


    return {"final_decision": decision,
            "retrieved_policies":policies}

