from pydantic import BaseModel


class Token(BaseModel):
    email: str
    role: int
    access_token: str
    token_type: str