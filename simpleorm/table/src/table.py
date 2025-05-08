from simpleorm.table.base import TableBase
from .filter import Filter
import numpy

class Table(TableBase):
    
    def __init__(self,conn,table_name):
        super().__init__(conn,table_name)
        
        self.result = self.get_all()
   
    def filter(self):
        return Filter(self.conn,self.table_name)
    
    def get_all(self):
        query = f"""SELECT * FROM {self.table_name}"""
        try: 
            self.cursor.execute(query)
            self.result =  self.cursor.fetchall()
            return self.result
        except Exception as e:
            raise e
    
    def get(self,where_col=None, value=None):
        if where_col is None:
            raise ValueError("'where' key is required to specify the condition column")
        
        if not value:
            raise ValueError("No value provided to update to where condition to change the specific row")
        
        query = f"""SELECT * FROM {self.table_name} WHERE {where_col} = {self.place_holder}"""
        try: 
            self.cursor.execute(query, (value,))
            self.result = self.cursor.fetchone()
            return self.result
        except Exception as e:
            raise e
        
    def post(self, exec_vals :dict):
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
        
    def post_many(self, data:dict):
        if not data:
            return "No data to insert."
        
        if isinstance(data, dict):
            try:
                col_lengths = [len(v) for v in data.values()]
                if len(set(col_lengths)) != 1:
                    raise ValueError("All columns must have the same number of values.")
                
                data = [dict(zip(data.keys(), values)) for values in zip(*data.values())]
                
            except Exception as e:
                raise ValueError(f"Invalid column-wise input: {e}")
        
        insert_cols = list(data[0].keys())
        insert_col_str = ", ".join(insert_cols)    
            
        placeholders = ', '.join([self.place_holder] * len(insert_cols))
        query = f"INSERT INTO {self.table_name} ({insert_col_str}) VALUES ({placeholders});"
        
        values = [tuple(row[col] for col in insert_cols) for row in data]

        try:
            self.cursor.executemany(query, values)
            self.conn.commit()
            return f"Inserted {len(values)} rows into '{self.table_name}'." 
        except Exception as e:
            self.conn.rollback()
            raise e
    
    def delete(self, **kwargs):
        if not kwargs:
            raise ValueError("No fields to update were provided")
        
        if len(kwargs) > 1:
            raise ValueError(f"expected only one argumment but got {len(kwargs)}")
        
        key = list(kwargs.keys())[0]
        value = tuple(kwargs.values())[0]
        
        if self.get(where_col = key, value=value) is None:
            raise ValueError(f"{key} = {value} record doent exist")
        
        query = f"""DELETE FROM {self.table_name} WHERE {key} = {self.place_holder}"""
        try:
            self.cursor.execute(query, (value,))
            self.conn.commit()
            return f"row deleted succesfully"
        
        except Exception as e:
            self.conn.rollback()
            raise e
        
    def update(self, where = None, value = None, **kwargs):
        if where is None:
            raise ValueError("'where' key is required to specify the condition column")
        
        if not value:
            raise ValueError("No value provided to update to where condition to change the specific row")
        
        if self.get(where_col=where,value=value) is None:
            raise ValueError(f"{where} = {value} record doent exist")
        
        update_clause = ', '.join([f"{key} = {self.place_holder}" for key in kwargs.keys()])
        query = f"UPDATE {self.table_name} SET {update_clause} WHERE {where} = {self.place_holder}"
        
        try:
            values = list(kwargs.values())
            values.append(value)
            self.cursor.execute(query, tuple(values))
            self.conn.commit()
            return f"row updated where {where} = {value} to {list(kwargs.keys())} to {list(kwargs.values())}"
        
        except Exception as e:
            self.conn.rollback()
            raise e