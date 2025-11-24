from typing import Dict, Any

DATABASE_SHARDS: Dict[str, Dict[str, Any]] = {
    "shard_0": {
        "HOST": "localhost",
        "PORT": 5432,
        "DB": "shard_0",
        "USER": "admin",
        "PASSWORD": "pass"
    },
    "shard_1": {
        "HOST": "localhost",
        "PORT": 5432,
        "DB": "shard_1",
        "USER": "admin",
        "PASSWORD": "pass"
    }
}

SHARD_COUNT = len(DATABASE_SHARDS)
