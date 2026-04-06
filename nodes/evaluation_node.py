import json
import os
from datetime import datetime
def evaluation_node(state,llm):

    print("\nInside Evaluation Node")

    final_json = state.get("final_prior_auth")
    policies   = state.get("retrieved_policies")
    decision   = state.get("final_decision")
    if not decision:
        print("No decision to evaluate")
        return {"validated_decision": None}


    prompt = f"""
You are a strict validation agent.

Your job is to VERIFY the decision, not create one.

Rules:
- Use ONLY provided policy text
- Infer conditions ONLY if strongly supported by patient data
- Ignore irrelevant policy sections
- If clearly satisfied → APPROVED
- If clearly violated → DENIED
- If truly missing → NEED_MORE_INFO

Return ONLY JSON:

{{
  "valid": true/false,
  "final_decision": "APPROVED / DENIED / NEED_MORE_INFO",
  "issues": ["list of problems"]
}}

Patient Case:
{json.dumps(final_json)}

Policies:
{json.dumps(policies)}

LLM Decision:
{json.dumps(decision)}
"""

    response = llm.chat(
        "You are a strict healthcare validator.",
        prompt
    )

    try:
        result = json.loads(response)
    except Exception as e:
        print(f"Validation parse error: {e}")
        result = {
            "valid": False,
            "final_decision": "NEED_MORE_INFO",
            "issues": ["Failed to parse validation response"]
        }

    print(f"Validation Result: {result}")

    



    os.makedirs("output", exist_ok=True)
    filename = f"output/final_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    final_output = {
        "input": final_json,
        "retrieved_policies": policies,
        "original_decision": decision,
        "validation": result,
        "final_decision": result["final_decision"]
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=4, ensure_ascii=False)




    return {
    "validated_decision": result,
    "final_decision": {
        "decision": result["final_decision"],
        "validated": result["valid"],
        "issues": result["issues"]
    }
}