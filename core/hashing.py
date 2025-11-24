from typing import Any


def shard_hash(key: Any, shard_count: int) -> int:
    """
    Deterministic hashing technique to pick a shard.

    Args:
        key: Anything uniquely identifying an object (user_id, tenant_id, etc.)
        shard_count: number of database shards configured

    Returns:
        index of shard (0..n-1)
    """
    return hash(str(key)) % shard_count
