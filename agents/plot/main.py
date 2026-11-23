
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Plot Agent", version="1.0.0")


class StoryRequest(BaseModel):
    story: str = Field(min_length=1)


@app.get("/health")
def health():
    return {
        "agent": "Plot Agent",
        "status": "running"
    }


@app.post("/generate")
def generate_plot(request: StoryRequest):

    story = request.story.strip()

    if not story:
        return {
            "agent": "Plot Agent",
            "plot": "Please provide a story idea."
        }

    if "island" in story.lower():
        plot = (
            "An explorer arrives on a mysterious island, "
            "discovers an ancient temple, and must solve "
            "a puzzle to escape safely."
        )
    else:
        plot = (
            f"{story} The main character faces an unexpected "
            "challenge and learns an important lesson."
        )

    return {
        "agent": "Plot Agent",
        "plot": plot
    }
