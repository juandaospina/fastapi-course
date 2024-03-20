from pydantic import BaseModel, Field


class RoleBodySchema(BaseModel):
    role_name: str = Field(min_length=3, max_length=20)
    is_active: bool = Field(default=True)
