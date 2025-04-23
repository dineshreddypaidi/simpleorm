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
    
    def drop_table(self, table_name):
        try:
            with self.get_cursor() as cursor:
                cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            self.commit()
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to drop table {table_name}: {e}")