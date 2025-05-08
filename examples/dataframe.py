from simpleorm.db import Connector
from simpleorm.config import *

mysql_config = load_json_config("config/connection_mysql_config.json")
postgres_config = load_json_config("config/connection_postgres_config.json")


db1 = Connector(postgres_config).connect()

tables = db1.show_tables()

print(tables)
user_table = db1.use_table(tables[0])



print(user_table.columns)

# print(user_table.result)

print(user_table.to_df())

