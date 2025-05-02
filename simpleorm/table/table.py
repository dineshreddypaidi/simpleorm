

class Filter():
    def __init__(self,table_name):
        self.conditions = []
        self.joins = []
        
        self.result = None
        self.query = None
        
        
    def __str__(self):
        return f"{self.result}"


class Table:
    def __init__(self,conn,table_name):
        self.conn = conn
        self.table_name = table_name
        self.place_holder = self.__place_holder()
        self.cursor = conn.cursor()

    def __place_holder(self):
        conn_type = self.conn.__class__.__module__
        if "sqlite3" in conn_type or "sqlite" in conn_type:
            return "?"
        else:
            return "%s"

    def get(self):
        query = f"""SELECT * FROM {self.table_name}"""
        self.cursor.execute(query)
        self.result =  self.cursor.fetchall()
        return self.result

    def post(self, exec_vals : dict):
        placeholders = ', '.join([self.place_holder] * len(exec_vals))
        query = f"INSERT INTO {self.table_name} ({" , ".join(list(exec_vals.keys()))}) VALUES ({placeholders});"
        try:
            self.cursor.execute(query, list(exec_vals.values()))
            self.conn.commit()
            return f"inserted succesfully into {self.table_name} values {list(exec_vals.values())}"
        except Exception as e:
            raise e
        
    def delete():
        pass
    
    def update(self):
        pass
    
    
    def __str__(self):
        return f"{self.result}"
    
