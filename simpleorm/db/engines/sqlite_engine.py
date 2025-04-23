import sqlite3
from simpleorm.db.base import BaseConnector
        
  
class SqliteConnector(BaseConnector):
    
    def get_connection(self):
        db_path = self.config.get("database", "db.sqlite3")
        self.conn = sqlite3.connect(db_path)

    def show_tables(self):
        cursor = self.get_cursor()
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        
        return tables