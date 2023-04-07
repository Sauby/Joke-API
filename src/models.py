from sqlalchemy import Integer, Column, String
from db import Base

# The model for the joke api
class Jokes(Base):
    __tablename__ = "jokes"

    id = Column(Integer, primary_key=True, index=True,)
    category = Column(String)
    joke = Column(String)
    likes = Column(Integer)
   