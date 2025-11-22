from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.db.database_setup import engine
from app.models.models import User, ResponseGlobal, LoginBody, AuthorizationResponse
from app.services.encryption_service import password_hash, checking_password, create_jwt_token
from datetime import datetime, timedelta, timezone

router = APIRouter(
    prefix="/login",
    tags=["Auth"]
)

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/sign-in", status_code=200)
async def sign_in(body: LoginBody, session: Session = Depends(get_session)):
    query = select(User).where(User.email == body.email)
    user_found = session.exec(query).one()

    is_correct_pw = checking_password(body.password, user_found.password)
    user_dict = user_found.model_dump(exclude={"password"})
    id = str(user_dict["id"])
    user_dict["id"] = id
    user_dict["exp"] = int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp())

    if is_correct_pw:
        token = create_jwt_token(user_dict)
        user_dict["token"] = token

    auth_response = AuthorizationResponse(
        user_id=user_dict["id"],
        name=user_dict["name"],
        email=user_dict["email"],
        exp=user_dict["exp"],
        token=user_dict["token"]
    )

    return ResponseGlobal(success=True, message="Se logeó exitosamente", data=auth_response)

@router.post("/register", status_code=201)
async def register(body: User, session: Session = Depends(get_session)) -> ResponseGlobal :
    pw = body.password
    hash_pw = password_hash(pw)
    body.password = hash_pw
    
    session.add(body)
    session.commit()
    session.refresh(body)

    return ResponseGlobal(success=True, message="Se registró el usuario exitosamente", data=body)