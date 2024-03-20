from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    role: str
    phone_number: str = Field(min_length=12, max_length=13)


class UserPOSTSchema(UserSchema, BaseModel):
    password: str = Field(min_length=6)


class UserPUTSchema(BaseModel): 
    email: str | None 
    username: str | None 
    first_name: str | None 
    last_name: str | None 
    role: str | None 
    phone_number: str | None = Field(min_length=12, max_length=13)


# Change implementations to UserPOSTSchema 
class UserBodySchema(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str = Field(min_length=6)
    role: str
    phone_number: str = Field(min_length=12, max_length=13)


class UserResetPasswordSchema(BaseModel):
    password: str
    new_password: str = Field(min_length=6)
