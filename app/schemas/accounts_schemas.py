from pydantic import BaseModel, EmailStr, constr


class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=48)

    class Config:
        json_schema_extra = {
            "example": {"email": "user@example.com", "password": "securepassword123"}
        }


class TokenRefresh(BaseModel):
    refresh: constr(min_length=1)

    class Config:
        json_schema_extra = {
            "example": {"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
        }
