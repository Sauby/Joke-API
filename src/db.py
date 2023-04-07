from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# giving the url to the database
JOKES_DATABASE_URL = "sqlite:///./books.db"

# creating the engine for the database
engine = create_engine(JOKES_DATABASE_URL, connect_args={"check_same_thread":False})

# creating the sessions in order for database to act
sessionLocal = sessionmaker(bind=engine, autoflush=False)

# declaring base
Base = declarative_base()