# GraphBuilder.py

from functools import partial
from langgraph.graph import StateGraph, END

from nodes.form_node import form_node
from nodes.labs_node import labs_node
from nodes.imaging_node import imaging_node
from nodes.notes_node import notes_node
from nodes.orchestrator_node import orchestrator_node
from nodes.aggregator_node import aggregator_node
from nodes.policy_node import policy_node
from nodes.index_node import index_node
from nodes.evaluation_node import evaluation_node

from State import PriorAuthState

from llm.mistral import LLMClient
from llm.gemini import LLMClient as GeminiClient

from ocr.ocr_space import OCRSpaceClient
from embeddings.huggingface_embedding import HFEmbeddings
from vectordb.chormadb import ChromaDB


def route_from_orchestrator(state):
    if state.get("index_ready"):
        return "trigger"
    return "index"


def build_graph():

    # ── Create ALL objects ONCE here ──────────────────────────────────
    llm      = LLMClient()
    gemini=GeminiClient()
    ocr      = OCRSpaceClient()
    embedder = HFEmbeddings()
    vectordb = ChromaDB(embedder=embedder)

    workflow = StateGraph(PriorAuthState)

    # ── Nodes ──────────────────────────────────────────────────────────
    workflow.add_node("orchestrator", partial(orchestrator_node, vectordb=vectordb))
    workflow.add_node("index",        partial(index_node,     vectordb=vectordb))
    workflow.add_node("trigger",      lambda state: {})

    workflow.add_node("form",         partial(form_node,      llm=llm, ocr=ocr))
    workflow.add_node("labs",         partial(labs_node,      llm=llm, ocr=ocr))
    workflow.add_node("imaging",      partial(imaging_node,   llm=llm, ocr=ocr))
    workflow.add_node("notes",        partial(notes_node,     llm=llm, ocr=ocr))

    workflow.add_node("aggregator",   partial(aggregator_node, llm=llm))
    workflow.add_node("policy",       partial(policy_node,    llm=llm, vectordb=vectordb))
    workflow.add_node("evaluation",   partial(evaluation_node, llm=llm))



    # ── Entry ──────────────────────────────────────────────────────────
    workflow.set_entry_point("orchestrator")

    # ── Conditional routing ────────────────────────────────────────────
    workflow.add_conditional_edges(
        "orchestrator",
        route_from_orchestrator,
        ["index", "trigger"]
    )

    # ── After index → trigger ──────────────────────────────────────────
    workflow.add_edge("index", "trigger")

    # ── Fan out ────────────────────────────────────────────────────────
    workflow.add_edge("trigger", "form")
    workflow.add_edge("trigger", "labs")
    workflow.add_edge("trigger", "imaging")
    workflow.add_edge("trigger", "notes")

    # ── Fan in ─────────────────────────────────────────────────────────
    workflow.add_edge("form",    "aggregator")
    workflow.add_edge("labs",    "aggregator")
    workflow.add_edge("imaging", "aggregator")
    workflow.add_edge("notes",   "aggregator")

    # ── Final ──────────────────────────────────────────────────────────
    workflow.add_edge("aggregator", "policy")
    workflow.add_edge("policy", "evaluation")
    workflow.add_edge("evaluation", END)

    return workflow.compile()