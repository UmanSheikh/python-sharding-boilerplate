# Python Database Sharding Boilerplate

A comprehensive, production-ready boilerplate for implementing database sharding in Python applications using Django, Flask, and FastAPI frameworks.

This repository accompanies the article: **[Mastering Database Sharding with Python: Django, Flask, and FastAPI](https://www.linkedin.com/pulse/mastering-database-sharding-python-django-flask-fastapi-uman-sheikh-2avnc/?trackingId=V1ZmhkBvKfuWTxCIVn122g%3D%3D)** by Uman Sheikh.

## 📚 Overview

Database sharding is a critical technique for scaling applications horizontally by distributing data across multiple database instances. This boilerplate provides ready-to-use implementations of sharding strategies across three popular Python web frameworks.

## ✨ Features

- **Framework Agnostic Core**: Reusable sharding logic that works with any Python framework
- **Hash-based Sharding**: Deterministic shard selection using consistent hashing
- **Multiple Framework Support**: 
  - Django with database routers
  - Flask with SQLAlchemy
  - FastAPI with SQLAlchemy
- **Production Ready**: Clean, typed, and well-documented code
- **Extensible**: Easy to customize for your specific needs

## 🏗️ Architecture

The boilerplate uses a **hash-based sharding** strategy where data is distributed across shards based on a sharding key (e.g., `user_id`, `tenant_id`). The hash function ensures deterministic routing - the same key always maps to the same shard.

```
┌─────────────┐
│   Request   │
│  (user_id)  │
└──────┬──────┘
       │
       ▼
┌──────────────┐
│ Shard Router │  ← hash(user_id) % shard_count
└──────┬───────┘
       │
       ├─────────┬─────────┐
       ▼         ▼         ▼
   ┌────────┐ ┌────────┐ ┌────────┐
   │Shard 0 │ │Shard 1 │ │Shard N │
   └────────┘ └────────┘ └────────┘
```

## 📁 Project Structure

```
.
├── core/
│   ├── hashing.py          # Hash function for shard selection
│   ├── settings.py         # Database shard configurations
│   └── shard_router.py     # Main routing logic
├── django_app/
│   ├── routers.py          # Django database router implementation
│   └── settings_snippet.py # Django settings configuration
├── fastapi_app/
│   ├── db.py               # FastAPI database session management
│   └── main.py             # FastAPI application example
└── flask_app/
    ├── db.py               # Flask database session management
    └── app.py              # Flask application example
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL (or your preferred database)
- Virtual environment tool (venv, virtualenv, or conda)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/UmanSheikh/python-sharding-boilerplate.git
cd python-sharding-boilerplate
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies (based on your framework):
```bash
# For Django
pip install django psycopg2-binary

# For Flask
pip install flask sqlalchemy psycopg2-binary

# For FastAPI
pip install fastapi sqlalchemy psycopg2-binary uvicorn
```

4. Set up your database shards:
   - Create multiple database instances (e.g., `shard_0`, `shard_1`)
   - Update `core/settings.py` with your database credentials

## 💻 Usage

### Core Module

The core module provides framework-agnostic sharding logic:

```python
from core.shard_router import route_to_shard

# Route to appropriate shard based on user_id
user_id = 12345
shard_config = route_to_shard(user_id)
print(shard_config)
# Output: {'HOST': 'localhost', 'PORT': 5432, 'DB': 'shard_1', ...}
```

### Django Implementation

1. Add the router to your Django settings:
```python
# settings.py
DATABASE_ROUTERS = ["django_app.routers.ShardedRouter"]

DATABASES = {
    "default": {},
    "shard_0": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "shard_0",
        "USER": "admin",
        "PASSWORD": "pass",
        "HOST": "localhost",
        "PORT": 5432,
    },
    "shard_1": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "shard_1",
        "USER": "admin",
        "PASSWORD": "pass",
        "HOST": "localhost",
        "PORT": 5432,
    },
}
```

2. Use the router in your views:
```python
from django.db import models
from core.hashing import shard_hash
from core.settings import SHARD_COUNT

# Determine the shard for the user
shard_index = shard_hash(user_id, SHARD_COUNT)
shard_name = f"shard_{shard_index}"

# Query with explicit shard
User.objects.using(shard_name).create(
    name="John Doe"
)
```

### Flask Implementation

```python
from flask import Flask, request
from flask_app.db import get_session
from flask_app.models import User
from core.hashing import shard_hash
from core.settings import SHARD_COUNT

app = Flask(__name__)

@app.post("/users")
def create_user():
    data = request.get_json()
    user_id = data["id"]
    
    # Get session for the appropriate shard
    session = get_session(user_id)
    
    user = User(id=user_id, name=data["name"])
    session.add(user)
    session.commit()
    
    # Calculate which shard was used
    shard_index = shard_hash(user_id, SHARD_COUNT)
    
    return {"status": "ok", "shard": shard_index}

if __name__ == "__main__":
    app.run()
```

### FastAPI Implementation

```python
from fastapi import FastAPI
from fastapi_app.db import get_session
from fastapi_app.models import User
from core.hashing import shard_hash
from core.settings import SHARD_COUNT

app = FastAPI()

@app.post("/users")
def create_user(id: int, name: str):
    # Get session for the appropriate shard
    session = get_session(id)
    
    user = User(id=id, name=name)
    session.add(user)
    session.commit()
    
    # Calculate which shard was used
    shard_index = shard_hash(id, SHARD_COUNT)
    
    return {"stored_in_shard": shard_index}
```

Run with:
```bash
uvicorn fastapi_app.main:app --reload
```

## ⚙️ Configuration

### Customizing Shard Configuration

Edit `core/settings.py` to add or modify shards:

```python
DATABASE_SHARDS = {
    "shard_0": {
        "HOST": "localhost",
        "PORT": 5432,
        "DB": "shard_0",
        "USER": "admin",
        "PASSWORD": "pass"
    },
    "shard_1": {
        "HOST": "db-server-2",
        "PORT": 5432,
        "DB": "shard_1",
        "USER": "admin",
        "PASSWORD": "pass"
    },
    # Add more shards as needed
}
```

### Custom Hash Function

You can implement your own hashing strategy in `core/hashing.py`:

```python
def shard_hash(key: Any, shard_count: int) -> int:
    # Custom hashing logic
    return custom_hash(key) % shard_count
```

## 🔍 How Sharding Works

1. **Key Selection**: Choose a sharding key (e.g., `user_id`, `tenant_id`) that evenly distributes data
2. **Hash Calculation**: Apply hash function to the key: `hash(key) % shard_count`
3. **Shard Routing**: Map the hash result to a specific database shard
4. **Connection**: Establish connection to the selected shard
5. **Operation**: Perform database operations on the correct shard

### Benefits

- **Horizontal Scalability**: Add more shards to handle increased load
- **Performance**: Smaller datasets per shard result in faster queries
- **Isolation**: Issues in one shard don't affect others
- **Geographic Distribution**: Place shards closer to users

### Considerations

- **Cross-shard Queries**: Complex queries across shards require special handling
- **Rebalancing**: Adding/removing shards requires data migration
- **Transactions**: Cross-shard transactions need distributed transaction support
- **Complexity**: Additional operational overhead

## 📖 Learn More

For a deep dive into database sharding concepts and implementation details, read the full article:

**[Mastering Database Sharding with Python: Django, Flask, and FastAPI](https://www.linkedin.com/pulse/mastering-database-sharding-python-django-flask-fastapi-uman-sheikh-2avnc/?trackingId=V1ZmhkBvKfuWTxCIVn122g%3D%3D)**

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Uman Sheikh**

- LinkedIn: [@uman-sheikh](https://www.linkedin.com/in/uman-sheikh/)
- GitHub: [@UmanSheikh](https://github.com/UmanSheikh)

## 🙏 Acknowledgments

- Inspired by real-world scaling challenges in production systems
- Built to help developers implement sharding without reinventing the wheel
- Thanks to the Python community for excellent frameworks and tools

---

⭐ If you find this boilerplate helpful, please consider giving it a star on GitHub!
