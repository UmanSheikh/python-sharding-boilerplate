from typing import Any
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from core.shard_router import route_to_shard


def get_session(key: Any):
    shard = route_to_shard(key)
    uri = f"postgresql://{shard['USER']}:{shard['PASSWORD']}@{shard['HOST']}/{shard['DB']}"

    engine = create_engine(uri)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()
