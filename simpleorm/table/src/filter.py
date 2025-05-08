from simpleorm.table.base import TableBase

class Filter(TableBase):
    def __init__(self,conn,table_name):
        super().__init__(conn,table_name)
 
        self.set_limit = None
        self.set_where = []
      
        self.set_columns = []
        self.result = None
        
    def __query_builder(self):
        cols = ", ".join(self.set_columns) if self.set_columns else "*"

        query = f"""
            SELECT {cols} from {self.table_name}
        """
        if self.set_where:
            query += " WHERE " + " AND ".join(self.set_where)

        if self.set_limit:
            query += f" LIMIT {self.set_limit}"

        return query + ";"
        
    def __set_result(self):
        if self.set_columns:
            self.columns = self.set_columns
        query = self.__query_builder()
        try:
            self.cursor.execute(query)
            res = self.cursor.fetchall()
            self.result = res
            return self.result
        except Exception as e:
            raise e
        
    @property
    def fetch(self):
        if self.result is None:
            self.__set_result()
        return self
    
    def column(self,value):
        if value not in self.set_columns:
            self.set_columns.append(value)
        return self
    
    def limit(self,value):
        self.set_limit = value
        return self
    
    def where(self,value):
        self.set_where.append(value)
        return self

    def __str__(self):
        return f"{self.__set_result()}"