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
        cursor.execute("SHOW TABLES;")
        return [row[0] for row in cursor.fetchall()]

    def __sql_format_for_col(self,col : dict):
        parts =  [col["column_name"],col["sql_type"]]
        if not col.get("not_null"):
            parts.append("NOT NULL")
        if col.get("is_primary"):
            parts.append("PRIMARY KEY")
        if col.get("is_unique"):
            parts.append("UNIQUE")
        if col.get("foreign_key"):
            parts.append(col["foreign_key"])
        if col.get("auto_increment"):
            parts.append("AUTO_INCREMENT")
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
                cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            self.commit()
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to drop table {table_name}: {e}")
        
    def truncate_table(self,table_name):
        try:
            with self.get_cursor() as cursor:
                query = f"""TRUNCATE TABLE {table_name};"""
                cursor.execute(query)
            self.commit()
            return f"{table_name} values are deleted"
        except Exception as e:
            raise RuntimeError(f"Failed to truncate table {table_name}: {e}")
        
             