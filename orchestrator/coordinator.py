from langgraph.graph import StateGraph, END, START
from agents.supervisor_agent import supervisor_agent
from agents.address_agent import address_agent
from agents.upsell_agent import upsell_recommendation_agent
from agents.chat_agent import chat_agent
from state.state import State

graph = StateGraph(State)

graph.add_node("supervisor", supervisor_agent)
graph.add_node("address", address_agent)
graph.add_node("upsell", upsell_recommendation_agent)
graph.add_node("chat", chat_agent)

graph.set_entry_point("supervisor")

app = graph.compile()