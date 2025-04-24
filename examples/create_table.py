import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from simpleorm.db import Connector
import json

def mysql_db_config():
    with open("../simpleorm/tests/config/connection_mysql_config.json", "r") as f:
        config = json.load(f)
    return config

def postgres_db_config():
    with open("../simpleorm/tests/config/connection_postgres_config.json", "r") as f:
        config = json.load(f)
    return config

db1 = Connector(postgres_db_config()).connect()

db2 = Connector(mysql_db_config()).connect()


table = {
    "id" : int,
    "name" : str,
}