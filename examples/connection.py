import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from simpleorm.db import Connector

config = {
    "engine": "postgres",
    "user": "postgres",
    "password": "123456",
    "host": "localhost",
    "database": "postgres"
}

config2 = {
    "engine": "mysql",
    "user": "root",
    "password": "root",
    "host": "localhost",
    "database": "world"
}

# Connect to Postgres
db1 = Connector(config).connect()

# Connect to MySQL
db2 = Connector(config2).connect()

# Now you can safely call show_tables()
print("Tables:", db2.show_tables())