import bcrypt
import jwt
from app.models.models import AuthorizationResponse
from fastapi import Request
from fastapi import HTTPException

secret_key = "clave-secreta-ximenius123"
algorithm = 'HS256'

def password_hash(pw: str) -> str:
    bytes = pw.encode("utf-8")
    hash_pw = bcrypt.hashpw(bytes, bcrypt.gensalt())

    return hash_pw.decode("utf-8")


def checking_password(pw_input: str, pw_hashed: str) -> bool:
    user_bytes = pw_input.encode("utf-8")
    pw_hashed_bytes = pw_hashed.encode("utf-8")
    is_same_password = bcrypt.checkpw(user_bytes,  pw_hashed_bytes)

    return is_same_password

def create_jwt_token(payload) -> str:
    token = jwt.encode(payload, secret_key, algorithm=algorithm)

    return token

def validate_jwt_token(request: Request) -> AuthorizationResponse:
    auth = request.headers.get("authorization")

    try:
        if auth:
            token_formatted = auth.replace("Bearer ", "")
            decoded_payload = jwt.decode(token_formatted, secret_key, algorithms=[algorithm])
            token_decoded = AuthorizationResponse(
                user_id=decoded_payload["id"],
                name=decoded_payload["name"],
                email=decoded_payload["email"],
                exp=decoded_payload["exp"]
            )

            return token_decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired. Please log in again.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token. Access denied.")

    raise HTTPException(status_code=400, detail="Error en Autorización")