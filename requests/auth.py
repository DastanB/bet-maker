from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str


class UpdateUserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    phone_number: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
