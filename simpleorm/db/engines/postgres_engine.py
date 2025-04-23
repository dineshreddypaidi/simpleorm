import psycopg2
from simpleorm.db.base import BaseConnector

class PostgresConnector(BaseConnector):
    
    def get_connection(self):
        self.conn = psycopg2.connect(
            dbname = self.config["database"],
            user = self.config["user"],
            password = self.config["password"],
            host = self.config.get("host", "localhost"),
            port = self.config.get("port", 5432)
        )
    
    def show_tables(self):
        cursor = self.get_cursor()
        query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
        """
        cursor.execute(query)
        tables = [row[0] for row in cursor.fetchall()]
        
        return tables
    
    def drop_table(self, table_name):
        try:
            with self.get_cursor() as cursor:
                cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
            self.commit()
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to drop table {table_name}: {e}")