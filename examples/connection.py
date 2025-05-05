from simpleorm.db import Connector
from simpleorm.config import *

mysql_config = load_json_config("config/connection_mysql_config.json")
postgres_config = load_json_config("config/connection_postgres_config.json")

mysql_url  = load_from_url("mysql://root:root@localhost/world")

db1 = Connector(postgres_config).connect()

db2 = Connector(mysql_url).connect()


# SHOW TABLES;
print("Postgres Tables:", db1.show_tables())

print("Mysql Tables:", db2.show_tables())