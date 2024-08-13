from pydantic import BaseModel, EmailStr, constr

class UserLogin(BaseModel):
    email: EmailStr
    password: str #constr(min_length=8)

class TokenRefresh(BaseModel):
    refresh: constr(min_length=1)
