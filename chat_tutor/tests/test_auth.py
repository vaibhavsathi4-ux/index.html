from jose import jwt

from app.auth import (
    create_access_token,
    verify_token,
)

from app.config import settings


# -----------------------------------------------------
# Token Creation
# -----------------------------------------------------

def test_create_access_token():

    token = create_access_token("user123")

    assert token is not None

    assert isinstance(token, str)

    assert len(token) > 20


# -----------------------------------------------------
# Token Decode
# -----------------------------------------------------

def test_verify_token():

    token = create_access_token("user123")

    user = verify_token(token)

    assert user == "user123"


# -----------------------------------------------------
# Invalid Token
# -----------------------------------------------------

def test_invalid_token():

    token = "invalid.token.string"

    result = verify_token(token)

    assert result is None


# -----------------------------------------------------
# JWT Payload
# -----------------------------------------------------

def test_payload_contains_sub():

    token = create_access_token("student001")

    payload = jwt.decode(

        token,

        settings.JWT_SECRET,

        algorithms=[settings.JWT_ALGORITHM],

    )

    assert payload["sub"] == "student001"


# -----------------------------------------------------
# Expiration Exists
# -----------------------------------------------------

def test_payload_has_exp():

    token = create_access_token("student001")

    payload = jwt.decode(

        token,

        settings.JWT_SECRET,

        algorithms=[settings.JWT_ALGORITHM],

    )

    assert "exp" in payload


# -----------------------------------------------------
# Different Users
# -----------------------------------------------------

def test_multiple_users():

    token1 = create_access_token("user1")

    token2 = create_access_token("user2")

    assert token1 != token2

    assert verify_token(token1) == "user1"

    assert verify_token(token2) == "user2"


# -----------------------------------------------------
# Empty User
# -----------------------------------------------------

def test_empty_user():

    token = create_access_token("")

    assert verify_token(token) == ""


# -----------------------------------------------------
# Random Invalid Secret
# -----------------------------------------------------

def test_wrong_secret():

    token = create_access_token("abc")

    try:

        jwt.decode(

            token,

            "wrong-secret",

            algorithms=[settings.JWT_ALGORITHM],

        )

        assert False

    except Exception:

        assert True


# -----------------------------------------------------
# Authorization Header
# -----------------------------------------------------

def test_authorization_header(auth_headers):

    assert "Authorization" in auth_headers

    assert auth_headers["Authorization"].startswith("Bearer ")