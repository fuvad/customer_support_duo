from fastapi import FastAPI, Body
from app.graph.support_graph import support_graph

app = FastAPI(title="Customer Support Duo")

@app.post("/ask")
async def ask_support(query: str = Body(...)):
    state = {"query": query}
    final_state = await support_graph.ainvoke(state)
    return {"response": final_state["response"]}

