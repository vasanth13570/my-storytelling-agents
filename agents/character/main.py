
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Character Agent", version="1.0.0")


class StoryRequest(BaseModel):
    story: str = Field(min_length=1)
    plot: str = ""


@app.get("/health")
def health():
    return {
        "agent": "Character Agent",
        "status": "running"
    }


@app.post("/generate")
def generate_character(request: StoryRequest):

    story = request.story.strip()
    plot = request.plot.strip()

    context = (story + " " + plot).lower()

    if "island" in context or "explorer" in context:
        characters = [
            {
                "name": "Alex",
                "role": "Explorer",
                "personality": "Brave and curious",
                "description": "A young explorer searching for adventure."
            },
            {
                "name": "Maya",
                "role": "Island Guardian",
                "personality": "Wise and mysterious",
                "description": "A guardian protecting the island's secrets."
            }
        ]
    else:
        characters = [
            {
                "name": "Sam",
                "role": "Main Character",
                "personality": "Determined and creative",
                "description": "A traveller facing an unexpected challenge."
            }
        ]

    return {
        "agent": "Character Agent",
        "characters": characters
    }
