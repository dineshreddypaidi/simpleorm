import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from simpleorm.db import Connector
from simpleorm.config import load_json_config

mysql_config = load_json_config("../config/connection_mysql_config.json")
postgres_config = load_json_config("../config/connection_postgres_config.json")


db1 = Connector(postgres_config).connect()

db2 = Connector(mysql_config).connect()


# SHOW TABLES;
print("Postgres Tables:", db1.show_tables())

print("Mysql Tables:", db2.show_tables())