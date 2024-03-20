from pydantic import BaseModel, Field

class TaskBodySchema(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    description: str = Field(min_length=2, max_length=255)
    priority: int = Field(gt=0, lt=6)
    complete: bool = Field(default=False)