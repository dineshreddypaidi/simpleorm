import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from simpleorm.db import Connector
from simpleorm.config import *


postgres_config = load_json_config("../config/connection_postgres_config.json")

db1 = Connector(postgres_config).connect()

print("Postgres Tables:", db1.show_tables())


user_table = db1.use_table(db1.show_tables()[0])

print(user_table.get())


quer_ = {
    "username" : "dinesh",
    "email" : "dineshreddy@gmaail.com",
    "password_hash" : "hfhgjhnhfcf"
}

user_table.post(quer_)

print(user_table.get())