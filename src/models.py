from pydantic import BaseModel, Field

EXAMPLE_INPUT = {
    "message": "Code to be analyzed, documented or improved.",
}

class Input(BaseModel):
    message: str = "Analyze this code."

class Output(BaseModel):
    result: str

class SearchInput(BaseModel):
    header: str = Field(description="Prompt to be used.")
