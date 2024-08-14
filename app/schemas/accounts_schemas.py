from pydantic import BaseModel, EmailStr, constr


class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=48)

    @classmethod
    def model_json_schema(cls, **kwargs):
        schema = super().model_json_schema()
        schema["examples"] = {
            "email": "user@example.com",
            "password": "securepassword123",
        }
        return schema


class TokenRefresh(BaseModel):
    refresh: constr(min_length=1)

    @classmethod
    def model_json_schema(cls, **kwargs):
        schema = super().model_json_schema()
        schema["examples"] = {"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
        return schema
