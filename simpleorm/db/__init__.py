from .connection import Connector

def connect_db(config :dict):
    return Connector(config).connect()