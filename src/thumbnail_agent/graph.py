from langgraph.graph import StateGraph,START,END
from thumbnail_agent.state import ThumbnailState
from thumbnail_agent.nodes.websearch import web_search
from thumbnail_agent.nodes.promptwriter import prompt_writer
from thumbnail_agent.nodes.generator import generator
from thumbnail_agent.nodes.critic import critic
from thumbnail_agent.nodes.saver import saver


def should_continue(state: ThumbnailState) -> str:
    rating = state["rating"]
    iteration = state["iteration"]
    target_rating = state["target_rating"]
    max_iterations = state["max_iterations"]
    print("\nChecking continuation condition...")
    if rating >= target_rating:
        print("Target rating achieved")
        return "saver"
    if iteration >= max_iterations:
        print("Maximum iterations reached")
        return "saver"
    print("Refinement required")
    return "prompt_writer"


def build_graph():
    workflow = StateGraph(ThumbnailState)
    # Register five nodes
    workflow.add_node("web_search",web_search)
    workflow.add_node("prompt_writer",prompt_writer)
    workflow.add_node("generator",generator)
    workflow.add_node("critic",critic)
    workflow.add_node("saver",saver)
    # Normal graph edges
    workflow.add_edge(START,"web_search")
    workflow.add_edge("web_search","prompt_writer")
    workflow.add_edge("prompt_writer","generator")
    workflow.add_edge("generator","critic")
    # Conditional refinement loop
    workflow.add_conditional_edges(
        "critic",
        should_continue,
        {
            "prompt_writer": "prompt_writer",
            "saver": "saver"
        }
    )

    workflow.add_edge("saver",END)

    # No checkpointer
    graph = workflow.compile()
    return graph