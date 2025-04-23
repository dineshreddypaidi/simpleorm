from simpleorm.db.engines import *

_ENGINE_MAP = {
    "sqlite": SqliteConnector,
    "sqlite3": SqliteConnector,
    "postgres": PostgresConnector,
    "postgresql" : PostgresConnector,
    "mysql": MySQLConnector,
}

class Connector:
    def __init__(self, config: dict):
        self.config = config
        engine = config.get("engine")
        if engine not in _ENGINE_MAP:
            raise ValueError(f"Unsupported engine: {engine}")
        self.connection = _ENGINE_MAP[engine](config)

    def connect(self):
        self.connection.connect()
        return self.connection
    