from fastapi import FastAPI
from fastapi_app.db import get_session
from fastapi_app.models import User


app = FastAPI()


@app.post("/users")
def create_user(id: int, name: str):
    session = get_session(id)

    user = User(id=id, name=name)
    session.add(user)
    session.commit()

    return {"stored_in_shard": id % 2}
