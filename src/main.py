from typing import Union
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from uuid import UUID
import models
from db import engine, sessionLocal
from sqlalchemy.orm import session

# creating rest API app
app = FastAPI()

# Binding the database 
models.Base.metadata.create_all(bind=engine)

# Calling the database to get executed
async def get_db():
    try:
        db = sessionLocal()
        yield db
    finally:
        db.close()


# The joke model
class Joke(BaseModel):
    id : UUID
    category : str = Field(min_length=1)
    joke : str = Field(min_length=1)
    likes : int = Field()


# Routes

# Get the jokes
@app.get("/")
async def get_joke(db : session = Depends(get_db)):
    return db.query(models.Jokes).all()


# Make a joke
@app.post("/")
async def make_joke(joke: Joke, db : session = Depends(get_db)):
    joke_model = models.Jokes()
    joke_model.category = joke.category
    joke_model.joke = joke.joke
    joke_model.likes = joke.likes

    db.add(joke_model)
    db.commit()



# update jokes
@app.put("/{joke_id}")
async def update_joke(joke: Joke, joke_id : int, db : session = Depends(get_db)):

    joke_model = db.query(models.Jokes).filter(models.Jokes.id == joke_id).first()

    if joke_model is None:
        raise HTTPException(status_code=404, detail=f"ID {joke_id} does not exist")
    
    joke_model.category = joke.category
    joke_model.joke = joke.joke
    joke_model.likes = joke.likes

    db.add(joke_model)
    db.commit()


# Delete jokes
@app.delete("/{joke_id}")
async def delete_joke(joke_id : int, db : session = Depends(get_db)):

    joke_model = db.query(models.Jokes).filter(models.Jokes.id == joke_id).first()

    if joke_model is None:
        raise HTTPException(status_code=404, detail=f"ID {joke_id} does not exist")

    joke_model = db.query(models.Jokes).filter(models.Jokes.id == joke_id).delete()

    db.commit()

