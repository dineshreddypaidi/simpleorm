import sqlite3
from simpleorm.db.base import BaseConnector
        
  
class SqliteConnector(BaseConnector):
    
    def get_connection(self):
        db_path = self.config.get("database", "db.sqlite3")
        self.conn = sqlite3.connect(db_path)

    def show_tables(self):
        cursor = self.get_cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
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
            parts.append("AUTOINCREMENT")
        if col.get("default"):
            parts.append(col["default"])  
        if col.get("is_auto"):
            parts.append("DEFAULT CURRENT_TIMESTAMP")
        #spl:
        if not col.get("not_null") and col.get("is_primary") and col.get("is_unique") and col.get("auto_increment"):
            parts = [col["column_name"],col["sql_type"], "PRIMARY KEY AUTOINCREMENT"]
             
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
            cursor = self.get_cursor()
            cursor.execute(query)
            self.commit()
            return f"Table created successfully in database"
            raise RuntimeError(f"cannot create table {table_name}: {e}")
        
    def drop_table(self, table_name):
        try:
            cursor = self.get_cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            self.commit()
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to drop table {table_name}: {e}")
        
    def truncate_table(self,table_name):
        try:
            cursor = self.get_cursor()
            query = f"""DELETE FROM {table_name};""" 
            cursor.execute(query)
            query = f"""DELETE FROM sqlite_sequence WHERE name='{table_name}';"""
            cursor.execute(query)
            self.commit()
            return f"{table_name} values are deleted"
        except Exception as e:
            raise RuntimeError(f"Failed to truncate table {table_name}: {e}")