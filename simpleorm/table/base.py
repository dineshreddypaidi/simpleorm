from abc import ABC

class TableBase(ABC):
    def __init__(self,conn,table_name):
        self.conn = conn
        self.table_name = table_name
        self.cursor = conn.cursor()

        self.place_holder = self.__place_holder()
        self.columns = self.__columns()
    
    def __columns(self):
        conn_type = self.conn.__class__.__module__
        if "sqlite3" in conn_type or "sqlite" in conn_type:
            query = f"PRAGMA table_info({self.table_name});"
            self.cursor.execute(query)
            columns = self.cursor.fetchall()
            column_names = [column[1] for column in columns]
            return column_names
        
        elif conn_type.startswith("mysql.connector"):
            query = f"""
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{self.table_name}'
                AND TABLE_SCHEMA = '{self.conn.database}';
            """
            self.cursor.execute(query)
            columns = self.cursor.fetchall()
            column_names = [column[0] for column in columns]
            return column_names
        
        elif conn_type.startswith("psycopg2"):
            self.cursor.execute("SELECT current_database();")
            db_name = self.cursor.fetchone()[0]
            
            query = f"""
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{self.table_name}'
                AND table_catalog = '{db_name}';
            """
            self.cursor.execute(query)
            columns = self.cursor.fetchall()
            column_names = [column[0] for column in columns]
            return column_names
        
        else:
            raise ValueError("not supported engine")
           
    def __place_holder(self):
        conn_type = self.conn.__class__.__module__
        if "sqlite3" in conn_type or "sqlite" in conn_type:
            return "?"
        else:
            return "%s"
            
    def to_df(self):
        import pandas as pd
        return pd.DataFrame(list(self.result), columns=self.columns)

    def to_csv(self,path):
        self.to_df().to_csv(path)
    