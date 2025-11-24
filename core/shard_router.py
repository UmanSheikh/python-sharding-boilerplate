from typing import Any, Dict
from core.hashing import shard_hash
from core.settings import DATABASE_SHARDS, SHARD_COUNT


def route_to_shard(key: Any) -> Dict[str, Any]:
    """
    Returns DB config for the shard mapped to the provided key.
    """
    index = shard_hash(key, SHARD_COUNT)
    shard_name = f"shard_{index}"
    return DATABASE_SHARDS[shard_name]
