from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "mysql+pymysql://root:01012007@localhost:3306/library_db"

engine = create_engine(DATABASE_URL)

LocalSession = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

class Base(DeclarativeBase):
    pass

def get_db():
    try:
        db = LocalSession()
        yield db
    finally:
        db.close()