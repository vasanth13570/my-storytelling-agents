
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Dialogue Agent", version="1.0.0")


class Character(BaseModel):
    name: str
    role: str
    personality: str
    description: str


class StoryRequest(BaseModel):
    story: str = Field(min_length=1)
    plot: str = ""
    characters: list[Character] = Field(default_factory=list)


@app.get("/health")
def health():
    return {
        "agent": "Dialogue Agent",
        "status": "running"
    }


@app.post("/generate")
def generate_dialogue(request: StoryRequest):

    if len(request.characters) >= 2:
        first = request.characters[0].name
        second = request.characters[1].name

        dialogues = [
            {
                "character": first,
                "message": "What should we do next?"
            },
            {
                "character": second,
                "message": "We must work together to overcome this challenge."
            }
        ]

    elif len(request.characters) == 1:
        first = request.characters[0].name

        dialogues = [
            {
                "character": first,
                "message": "I must find a way to complete this journey."
            }
        ]

    else:
        dialogues = [
            {
                "character": "Narrator",
                "message": "The adventure is about to begin."
            }
        ]

    return {
        "agent": "Dialogue Agent",
        "dialogues": dialogues
    }
