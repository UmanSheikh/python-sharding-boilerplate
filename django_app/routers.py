from typing import Optional, Type
from django.db.models import Model
from core.shard_router import route_to_shard


class ShardedRouter:
    """
    Routes models to database shards based on a sharding key (e.g., user_id).
    """
    def db_for_read(self, model: Type[Model], **hints) -> Optional[str]:
        key = hints.get("shard_key")
        if key is None:
            return None
        return f"shard_{key}"
    
    def db_for_write(self, model: Type[Model], **hints) -> Optional[str]:
        key = hints.get("shard_key")
        if key is None:
            return None
        return f"shard_{key}"
