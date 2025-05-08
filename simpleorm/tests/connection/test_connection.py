import pytest
from simpleorm.db import Connector
from simpleorm.config import load_json_config


@pytest.fixture
def postgres_db():
    postgres_config = load_json_config("./examples/config/connection_postgres_config.json")
    return Connector(postgres_config).connect()

@pytest.fixture
def mysql_db():
    mysql_config = load_json_config("./examples/config/connection_mysql_config.json")
    return Connector(mysql_config).connect()

def test_mysql_connection(mysql_db):
    assert mysql_db is not None, "Failed to connect to MySQL database"

def test_postgresql_connection(postgres_db):
    assert postgres_db is not None, "Failed to connect to PostgreSQL database"

def test_show_tables(postgres_db, mysql_db):
    assert isinstance(postgres_db.show_tables(), list)
    assert isinstance(mysql_db.show_tables(), list)



def test_delete_table(postgres_db, mysql_db):
    assert postgres_db.drop_table(table_name="users")
    assert mysql_db.drop_table(table_name="users")
