from pydantic import BaseModel, ConfigDict, Field



class SignInUserRequest(BaseModel):
    username: str
    password: str
