import pytest
from pydantic import ValidationError

from app.schemas.accounts_schemas import TokenRefresh, UserLogin


def test_user_login_valid_data():
    print("teeeeeeest" * 40)
    user_login = UserLogin(email="user@example.com", password="securepassword123")
    assert user_login.email == "user@example.com"
    assert user_login.password == "securepassword123"


def test_user_login_invalid_email():
    with pytest.raises(ValidationError):
        UserLogin(email="invalid-email", password="securepassword123")


def test_user_login_password_too_short():
    with pytest.raises(ValidationError):
        UserLogin(email="user@example.com", password="short")


def test_user_login_password_too_long():
    long_password = "a" * 49
    with pytest.raises(ValidationError):
        UserLogin(email="user@example.com", password=long_password)


def test_token_refresh_valid_data():
    token_refresh = TokenRefresh(refresh="valid_refresh_token")
    assert token_refresh.refresh == "valid_refresh_token"


def test_token_refresh_empty_token():
    with pytest.raises(ValidationError):
        TokenRefresh(refresh="")


def test_user_login_model_json_schema():
    schema = UserLogin.model_json_schema()
    assert schema["examples"] == {
        "email": "user@example.com",
        "password": "securepassword123",
    }


def test_token_refresh_model_json_schema():
    schema = TokenRefresh.model_json_schema()
    assert schema["examples"] == {"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
