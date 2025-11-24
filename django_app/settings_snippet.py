DATABASE_ROUTERS = ["django_app.routers.ShardedRouter"]

DATABASES = {
    "default": {},
    "shard_0": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "shard_0",
        "USER": "admin"
    },
    "shard_1": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "shard_1",
        "USER": "admin"
    }
}
