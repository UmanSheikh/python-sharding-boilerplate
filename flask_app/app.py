from flask import Flask
from flask_app.db import get_session
from flask_app.models import User

app = Flask(__name__)


@app.post("/users")
def create_user():
    payload = {"id": 42, "name": "Uman"}
    session = get_session(payload["id"])

    user = User(id=payload["id"], name=payload["name"])
    session.add(user)
    session.commit()

    return {"status": "ok", "shard": payload["id"] % 2}
