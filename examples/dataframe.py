from simpleorm.db import connect_db
from simpleorm.config import *

mysql_config = load_from_json("config/connection_mysql_config.json")
postgres_config = load_from_json("config/connection_postgres_config.json")


db1 = connect_db(mysql_config)

tables = db1.show_tables()

print(tables)
user_table = db1.use_table(tables[0])



print(user_table.columns)

# print(user_table.result)

print(user_table.to_df())

