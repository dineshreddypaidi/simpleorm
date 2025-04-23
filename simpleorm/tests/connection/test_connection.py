import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import pytest
import json
from simpleorm.db import Connector

def test_mysql_connection():

    with open("./simpleorm/tests/config/connection_mysql_config.json", "r") as f:
        config = json.load(f)

    db = Connector(config).connect()
    assert db is not None, "Failed to connect to MySQL database"
    assert db.show_tables() is not None, "Failed to retrieve tables from MySQL database"

def test_postgresql_connection():
    with open("./simpleorm/tests/config/connection_postgres_config.json", "r") as f:
        config = json.load(f)

    db = Connector(config).connect()
    assert db is not None, "Failed to connect to PostgreSQL database"
    assert db.show_tables() is not None, "Failed to retrieve tables from PostgreSQL database"       