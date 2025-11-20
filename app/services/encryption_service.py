import bcrypt
import jwt
from app.models.models import ResponseGlobal

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

def create_jwt_token(payload):
    token = jwt.encode(payload, secret_key, algorithm=algorithm)

    return token

def validate_jwt_token(request):
    auth = request.headers.get("authorization")
    token_formatted = auth.replace("Bearer ", "")

    try:
        decoded_payload = jwt.decode(token_formatted, secret_key, algorithms=[algorithm])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        return ResponseGlobal(success=False, message="Token has expired. Please log in again.", data=None)
    except jwt.InvalidTokenError:
        return ResponseGlobal(success=False, message="Invalid token. Access denied.", data=None)
