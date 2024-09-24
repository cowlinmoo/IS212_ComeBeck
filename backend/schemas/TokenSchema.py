from pydantic import BaseModel, Field


class Token(BaseModel):
    email: str = Field(examples=["test@gmail.com"])
    role: str = Field(examples=["HR", "STAFF", "MANAGER"])
    access_token: str = Field(examples=["access_token"])
    token_type: str = Field(examples=["bearer"])