from sqlmodel import create_engine, Session, SQLModel


DB_URL = "sqlite:///./e-learning.db"

engine = create_engine(DB_URL, echo=True)

def init_db():
  SQLModel.metadata.create_all(engine)
  
def get_session():
  with Session(engine) as session:
    yield session
    