from database import Base
from sqlalchemy import Column, Integer, String, Numeric

class BookModel(Base):
    __tablename__ = "books"
    id    = Column(Integer, primary_key=True, autoincrement=True)
    code  = Column(String(50), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    price = Column(Numeric(10,2), nullable=False, default=0)
    pages = Column(Integer, nullable=False, default=0)
