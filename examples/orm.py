from simpleorm.db import Connector
from simpleorm.config import *
from simpleorm.table import Table

mysql_config = load_json_config("config/connection_mysql_config.json")
postgres_config = load_json_config("config/connection_postgres_config.json")


db1 = Connector(postgres_config).connect()

print("Postgres Tables:", db1.show_tables())


user_table = db1.use_table(db1.show_tables()[0])

print(user_table.get_all())

post_values = {
    "username" : ["vhkvkddinesh","hsgdasdvnchgm"],
    "email" : ["dineshrevhgvddy@gmaail.com","anything@gmail.com"],
    "password_hash" : ["hfhgjhnhfcf","hfhgjhnhfcf"]
}

print(user_table.post_many(post_values))


print(user_table.get_all())

print(user_table.update(value="dinesh",where="username",username="dineshreddy"))

print(user_table.get(where_col="username",value="dineshreddy"))

print(user_table.delete(username="dineshreddy"))

print(user_table.get_all())