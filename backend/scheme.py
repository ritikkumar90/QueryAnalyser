from pydantic import BaseModel


class UserLogin(BaseModel):
    email: str
    password: str

class UserSignup(BaseModel):
    name: str
    email: str
    password: str

class QueryRequest(BaseModel):
    question: str
