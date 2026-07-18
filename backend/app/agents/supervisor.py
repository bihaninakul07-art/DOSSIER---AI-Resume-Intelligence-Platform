"""LangGraph orchestration: supervisor routes through parser -> extractor
-> [rag_agent, market_trend_agent] (parallel) -> critique -> recommendation
-> poster. Parallel branch + merge demonstrates the orchestrator-worker /
parallelization pattern; each node is independently retryable and the
graph state carries every intermediate artifact for the frontend to stream.
"""
from typing import TypedDict, Optional

from langgraph.graph import StateGraph, END

from app.agents.parser_agent import run_parser
from app.agents.extractor_agent import run_extractor
from app.agents.rag_agent import run_rag_agent
from app.agents.market_trend_agent import run_market_trend_agent
from app.agents.critique_agent import run_critique_agent
from app.agents.recommendation_agent import run_recommendation_agent
from app.imagegen.poster_generator import generate_poster
from app.models.schemas import (
    ParsedResume, ExtractedProfile, RetrievedContext, GapAnalysis, Recommendation,
)


class GraphState(TypedDict, total=False):
    pdf_bytes: bytes
    parsed: ParsedResume
    profile: ExtractedProfile
    context: list[RetrievedContext]
    market_notes: list[str]
    gap_analysis: GapAnalysis
    recommendation: Recommendation
    provider_notes: dict
    poster_url: Optional[str]


async def _node_parse(state: GraphState) -> GraphState:
    parsed = run_parser(state["pdf_bytes"])
    return {"parsed": parsed}


async def _node_extract(state: GraphState) -> GraphState:
    profile = await run_extractor(state["parsed"])
    return {"profile": profile}


async def _node_rag(state: GraphState) -> GraphState:
    context = await run_rag_agent(state["profile"])
    return {"context": context}


async def _node_market(state: GraphState) -> GraphState:
    notes = await run_market_trend_agent(state["profile"])
    return {"market_notes": notes}


async def _node_critique(state: GraphState) -> GraphState:
    gap = await run_critique_agent(
        state["profile"], state.get("context", []), state.get("market_notes", [])
    )
    return {"gap_analysis": gap}


async def _node_recommend(state: GraphState) -> GraphState:
    rec, provider_notes = await run_recommendation_agent(
        state["profile"], state["gap_analysis"], state.get("context", [])
    )
    return {"recommendation": rec, "provider_notes": provider_notes}


async def _node_poster(state: GraphState) -> GraphState:
    url = await generate_poster(state["recommendation"])
    return {"poster_url": url}


def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("parser", _node_parse)
    graph.add_node("extractor", _node_extract)
    graph.add_node("rag_agent", _node_rag)
    graph.add_node("market_trend_agent", _node_market)
    graph.add_node("critique", _node_critique)
    graph.add_node("recommendation_agent", _node_recommend)
    graph.add_node("poster", _node_poster)

    graph.set_entry_point("parser")
    graph.add_edge("parser", "extractor")
    # parallel branch: both run off extractor, both must finish before critique
    graph.add_edge("extractor", "rag_agent")
    graph.add_edge("extractor", "market_trend_agent")
    graph.add_edge("rag_agent", "critique")
    graph.add_edge("market_trend_agent", "critique")
    graph.add_edge("critique", "recommendation_agent")
    graph.add_edge("recommendation_agent", "poster")
    graph.add_edge("poster", END)

    return graph.compile()


compiled_graph = build_graph()


async def run_pipeline_streaming(pdf_bytes: bytes):
    """Async generator yielding (node_name, state_delta) as each node
    completes, so the API layer can push live SSE status events.
    """
    initial_state: GraphState = {"pdf_bytes": pdf_bytes}
    async for event in compiled_graph.astream(initial_state):
        for node_name, delta in event.items():
            yield node_name, delta
