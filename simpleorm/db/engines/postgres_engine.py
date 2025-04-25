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
    
    def __sql_format_for_col(self,col : dict):
        parts =  [col["column_name"],col["sql_type"]]
        if not col.get("not_null"):
            parts.append("NOT NULL")
        if col.get("auto_increment"):
            parts.append("GENERATED ALWAYS AS IDENTITY")
        if col.get("is_primary"):
            parts.append("PRIMARY KEY")
        if col.get("is_unique"):
            parts.append("UNIQUE")
        if col.get("foreign_key"):
            parts.append(col["foreign_key"])
        if col.get("default"):
            parts.append(col["default"])   
        if col.get("is_auto"):
            parts.append("DEFAULT CURRENT_TIMESTAMP")
        return " ".join(parts)
    
    def create_table(self,table_name : str, cols : dict):
        parts = []
        for col_name, col in cols.items():
            col_dict = col.to_sql(col_name)
            parts.append(self.__sql_format_for_col(col_dict))
                  
        query = f"""CREATE TABLE IF NOT EXISTS {table_name} (
                    {" , ".join(parts)}
                );"""
        
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query)
            self.commit()
            return f"Table creates succesful in {self.config["database"]} database"
        except Exception as e:
            raise RuntimeError(f"Failed to create table {table_name}: {e}")
    
    def drop_table(self, table_name):
        try:
            with self.get_cursor() as cursor:
                cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
            self.commit()
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to drop table {table_name}: {e}")
        
    def truncate_table(self,table_name):
        try:
            with self.get_cursor() as cursor:
                query = f"""TRUNCATE TABLE {table_name} RESTART IDENTITY;"""
                cursor.execute(query)
            self.commit()
            return f"{table_name} values are deleted"
        except Exception as e:
            raise RuntimeError(f"Failed to truncate table {table_name}: {e}")    