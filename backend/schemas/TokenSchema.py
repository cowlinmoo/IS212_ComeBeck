from pydantic import BaseModel, Field


class Token(BaseModel):
    email: str = Field(examples=["test@gmail.com"])
    role: int = Field(examples=[1, 2, 3])
    access_token: str = Field(examples=["access_token"])
    token_type: str = Field(examples=["bearer"])