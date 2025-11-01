from langgraph.graph import StateGraph, START, END
from app.agents.agents import SalesAgent, TechAgent
from typing import TypedDict, Optional

# Define the state schema
class SupportState(TypedDict):
    query: str
    response: Optional[str]
    next_agent: Optional[str]

sales = SalesAgent()
tech = TechAgent()

def sales_node(state):
    reply = sales.respond(state["query"])
    state["response"] = reply

    # Detect if we need to escalate to tech
    if "[ACTION: TRANSFER_TO_TECH]" in reply:
        state["next_agent"] = "tech"
    else:
        state["next_agent"] = "end"

    return state

def tech_node(state):
    reply = tech.respond(state["query"])
    state["response"] = reply
    state["next_agent"] = "end"
    return state

# --- Build dynamic flow ---
graph = StateGraph(SupportState)

graph.add_node("sales", sales_node)
graph.add_node("tech", tech_node)

graph.add_edge(START, "sales")

# Add conditional logic for branching
graph.add_conditional_edges(
    "sales",
    lambda state: state["next_agent"],  # decide next step dynamically
    {
        "tech": "tech",
        "end": END
    }
)

# Tech always ends
graph.add_edge("tech", END)

support_graph = graph.compile()

