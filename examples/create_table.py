from simpleorm.db import Connector
from simpleorm.config import load_json_config
from simpleorm.fields import *

mysql_config = load_json_config("config/connection_mysql_config.json")
postgres_config = load_json_config("config/connection_postgres_config.json")


db1 = Connector(postgres_config).connect()

db2 = Connector(mysql_config).connect()

db3 = Connector({"engine":"sqlite"}).connect()

sql_ = """CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL PRIMARY KEY UNIQUE AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)"""
        
cols = {
    "id" : IntegerField(primary_key=True),
    "username" : StringField(max_length=50,unique=True),
    "email" : StringField(max_length=100,unique=True),
    "password_hash" : TextField(),
    "created_at" : DateTimeField(auto=True,null=True)
}

print("postgres :")

print(db1.drop_table("users"))

print(db1.create_table("users",cols))

print(db1.show_tables())

print(db1.truncate_table("users"))

print("mysql :")

print(db2.drop_table("users"))

print(db2.create_table("users",cols))

print(db2.show_tables())

print(db2.truncate_table("users"))

print("sqlite :")

print(db3.drop_table("users"))

print(db3.create_table("users",cols))

print(db3.show_tables())

print(db3.truncate_table("users"))