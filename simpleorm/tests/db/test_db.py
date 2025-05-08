import pytest

from simpleorm.db import connect_db
from simpleorm.config import load_from_json,load_from_url

@pytest.fixture
def postgres_db():
    postgres_config = load_from_url("postgresql://postgres:123456@localhost:5432/postgres")
    return connect_db(postgres_config)

@pytest.fixture
def mysql_db():
    mysql_config = load_from_json("./examples/config/connection_mysql_config.json")
    return connect_db(mysql_config)

@pytest.fixture
def sqlite_db():
    return connect_db({"engine" : "sqlite3"})

def test_mysql_connection(mysql_db):
    assert mysql_db is not None, "Failed to connect to MySQL database"

def test_postgresql_connection(postgres_db):
    assert postgres_db is not None, "Failed to connect to PostgreSQL database"

def test_sqlite_connection(sqlite_db):
    assert sqlite_db is not None, "Failed to connect to sqlite database"

def test_show_tables(postgres_db, mysql_db):
    assert isinstance(postgres_db.show_tables(), list)
    assert isinstance(mysql_db.show_tables(), list)

def test_delete_table(postgres_db, mysql_db):
    assert postgres_db.drop_table(table_name="users")
    assert mysql_db.drop_table(table_name="users")
