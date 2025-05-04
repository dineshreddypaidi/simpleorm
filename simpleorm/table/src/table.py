from simpleorm.table.base import TableBase
from .filter import Filter

class Table(TableBase):
    
    def __init__(self,conn,table_name):
        self.conn = conn
        self.table_name = table_name
        self.place_holder = self.__place_holder()
        self.cursor = conn.cursor()
        
    @classmethod
    def filter_obj(cls,table_name):
        return Filter(table_name)
    
    def __place_holder(self):
        conn_type = self.conn.__class__.__module__
        if "sqlite3" in conn_type or "sqlite" in conn_type:
            return "?"
        else:
            return "%s"
      
    def filter(self):
        return Filter(self.table_name)
    
    def get_all(self):
        query = f"""SELECT * FROM {self.table_name}"""
        try: 
            self.cursor.execute(query)
            return  self.cursor.fetchall()
        except Exception as e:
            raise e
    
    def get(self,id):
        query = f"""SELECT * FROM {self.table_name} WHERE id = {self.place_holder}"""
        try: 
            self.cursor.execute(query, (id,))
            return  self.cursor.fetchone()
        except Exception as e:
            raise e
        
    def post(self, exec_vals : dict):
        placeholders = ', '.join([self.place_holder] * len(exec_vals))
        insert_col = ", ".join(list(exec_vals.keys()))
        query = f"INSERT INTO {self.table_name} ({insert_col}) VALUES ({placeholders});"
        try:
            self.cursor.execute(query, tuple(exec_vals.values()))
            self.conn.commit()
            return f"inserted succesfully into {self.table_name} values {list(exec_vals.values())}"
        except Exception as e:
            self.conn.rollback()
            raise e
        
    def delete(self, **kwargs):
        if not kwargs:
            raise ValueError("No fields to update were provided")
        
        if len(kwargs) > 1:
            raise ValueError(f"expected only one argumment but got {len(kwargs)}")
        
        cond_ = "".join(','.join([f"{key} = {self.place_holder}" for key in kwargs.keys()]))
        query = f"""DELETE FROM {self.table_name} WHERE {cond_}"""
        try:
            self.cursor.execute(query, tuple(kwargs.values()))
            self.conn.commit()
            return f"row deleted succesfully"
        
        except Exception as e:
            self.conn.rollback()
            raise e
        
    def update(self, value, **kwargs):
        if "where" not in kwargs:
            raise ValueError("'where' key is required to specify the condition column")

        where_column = kwargs.pop("where")
        if not kwargs:
            raise ValueError("No fields to update were provided")

        update_clause = ', '.join([f"{key} = {self.place_holder}" for key in kwargs.keys()])
        query = f"UPDATE {self.table_name} SET {update_clause} WHERE {where_column} = {self.place_holder}"
        
        try:
            values = list(kwargs.values())
            values.append(value)
            self.cursor.execute(query, tuple(values))
            self.conn.commit()
            return f"row updated where {where_column} = {value}"
        
        except Exception as e:
            self.conn.rollback()
            raise e