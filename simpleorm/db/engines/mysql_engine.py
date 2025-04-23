import mysql.connector
from simpleorm.db.base import BaseConnector

class MySQLConnector(BaseConnector):
    def get_connection(self):
        self.conn = mysql.connector.connect(
            host = self.config.get("host", "localhost"),
            user = self.config["user"],
            password = self.config["password"],
            database = self.config["database"],
            port = self.config.get("port",3306)
        )
        
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
            
        