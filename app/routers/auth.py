from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.db.database_setup import engine
from app.models.models import User

router = APIRouter(
    prefix="/api/v1",
    tags=["Auth"]
)

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/login/sign-in")
async def sign_in(session: Session = Depends(get_session)):
    
    return session.exec(select(User)).all()

@router.post("login/register")
async def register(session: Session = Depends(get_session)):
    return "Register"