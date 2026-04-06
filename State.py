from typing import TypedDict, List, Dict, Optional, Annotated


def merge_dicts(a: dict, b: dict) -> dict:
    if a is None:
        return b
    if b is None:
        return a
    return {**a, **b}


class PriorAuthState(TypedDict, total=False):

    pdfs: List[str]

    form_data: Annotated[Dict, merge_dicts]
    labs_data: Annotated[Dict, merge_dicts]
    imaging_data: Annotated[Dict, merge_dicts]
    notes_data: Annotated[Dict, merge_dicts]

    final_prior_auth: Annotated[Dict, merge_dicts]
    final_decision: Optional[Dict]
    retrieved_policies: List[Dict]
