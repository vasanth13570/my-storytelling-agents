
from typing import TypedDict
import json
import httpx

from langgraph.graph import StateGraph, START, END


# Shared information between agents
class StoryState(TypedDict):
    story: str
    plot: str
    characters: list[dict]
    dialogues: list[dict]


# Step 1: Call Plot Agent
def plot_node(state: StoryState):
    response = httpx.post(
        "http://127.0.0.1:9001/generate",
        json={"story": state["story"]},
        timeout=30.0
    )
    response.raise_for_status()

    return {
        "plot": response.json()["plot"]
    }


# Step 2: Call Character Agent
def character_node(state: StoryState):
    response = httpx.post(
        "http://127.0.0.1:9002/generate",
        json={
            "story": state["story"],
            "plot": state["plot"]
        },
        timeout=30.0
    )
    response.raise_for_status()

    return {
        "characters": response.json()["characters"]
    }


# Step 3: Call Dialogue Agent
def dialogue_node(state: StoryState):
    response = httpx.post(
        "http://127.0.0.1:9003/generate",
        json={
            "story": state["story"],
            "plot": state["plot"],
            "characters": state["characters"]
        },
        timeout=30.0
    )
    response.raise_for_status()

    return {
        "dialogues": response.json()["dialogues"]
    }


# Create LangGraph workflow
builder = StateGraph(StoryState)

builder.add_node("plot", plot_node)
builder.add_node("character", character_node)
builder.add_node("dialogue", dialogue_node)

# Define execution order
builder.add_edge(START, "plot")
builder.add_edge("plot", "character")
builder.add_edge("character", "dialogue")
builder.add_edge("dialogue", END)

# Compile the workflow
workflow = builder.compile()


if __name__ == "__main__":
    initial_state = {
        "story": "A young explorer discovers a mysterious island.",
        "plot": "",
        "characters": [],
        "dialogues": []
    }

    result = workflow.invoke(initial_state)

    print("\nFINAL STORYTELLING RESULT")
    print(json.dumps(result, indent=2))
