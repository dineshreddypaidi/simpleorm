# Usage Guide for simpleorm

Welcome! 👋  
 This guide will help you get started with using simpleorm in your project.

---

### 1. Set Up a Database

simpleorm supports multiple SQL engines.
Make sure you have a database running (or use a simple SQLite file).

Example for SQLite:

```python
DATABASE_URL = "sqlite:///your_database.db"

or

config = {
    "engine" : "sqlite3",
}
```

Example for PostgreSQL:

```python
DATABASE_URL = "postgresql://username:password@localhost/dbname"

or

config = {
    "engine" : "postgres",
    "user" : YOUR_USER_NAME,
    "password" : YOUR_PASSWORD,
    "host" : YOUR_DATABASE_HOST,
    "database" : YOUR_DATABASE
}

```

Example for MySQL:

```python
DATABASE_URL = "mysql://username:password@localhost/dbname"

or

config = {
    "engine" : "mysql",
    "user" : YOUR_USER_NAME,
    "password" : YOUR_PASSWORD,
    "host" : YOUR_DATABASE_HOST,
    "database" : YOUR_DATABASE
}
```

---

### 3. Initialize a Connection

```python
from simpleorm import connect

db = connect({
    "engine": "sqlite",
    "database": "your_database.db"
})

# Or for PostgreSQL
db = connect({
    "engine": "postgresql",
    "username": "yourusername",
    "password": "yourpassword",
    "host": "localhost",
    "port": 5432,
    "database": "yourdatabase"
})
```

---

### 4. Start Using SimpleORM!

```python
# Get a table
users = db.get_table("users")

# Create a new record
users.create(name="Alice", age=30)

# Query records
results = users.get(age=30)

# Update records
users.update({"name": "Alice Smith"}, where={"name": "Alice"})

# Delete records
users.delete(where={"age": 30})
```

---

## 🛠 Optional: Development Setup

If you want to contribute or run the latest development version:

```bash
git clone https://github.com/yourusername/simpleorm.git
cd simpleorm
pip install -e .
```

Install dev dependencies:

```bash
pip install -r requirements-dev.txt
```

Run tests:

```bash
pytest
```

---

## 📚 Documentation

Check the full docs here: [SimpleORM Documentation](https://github.com/yourusername/simpleorm/wiki)

---

Happy hacking with SimpleORM! 🚀
