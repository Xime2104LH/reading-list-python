from sqlmodel import create_engine, SQLModel

postgres_url = "postgresql://ximenahernandez:xime123@localhost:5432/ReadingList"

engine = create_engine(postgres_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)