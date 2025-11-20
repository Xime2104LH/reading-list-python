from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.db.database_setup import engine
from app.models.models import User, ResponseGlobal, LoginBody
from app.services.encryption_service import password_hash, checking_password, create_jwt_token
from datetime import datetime, timedelta, timezone

router = APIRouter(
    prefix="/api/v1",
    tags=["Auth"]
)

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/login/sign-in")
async def sign_in(body: LoginBody, session: Session = Depends(get_session)):
    query = select(User).where(User.email == body.email)
    user_found = session.exec(query).one()

    is_correct_pw = checking_password(body.password, user_found.password)
    user_dict = user_found.model_dump(exclude={"password"})
    user_dict["exp"] = datetime.now(timezone.utc) + timedelta(hours=1)
    print(user_dict)
    if is_correct_pw:
        token = create_jwt_token(user_dict)
        print(" TOKEN ", token)
        user_dict["token"] = token

    return {"success":True, "message":"Se logeó exitosamente", "data": user_dict}

@router.post("/login/register")
async def register(body: User, session: Session = Depends(get_session)) -> ResponseGlobal :
    pw = body.password
    hash_pw = password_hash(pw)
    body.password = hash_pw
    
    session.add(body)
    session.commit()
    session.refresh(body)

    return ResponseGlobal(success=True, message="Se registró el usuario exitosamente", data=body)