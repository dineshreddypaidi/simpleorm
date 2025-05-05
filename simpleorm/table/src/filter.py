from simpleorm.table.base import TableBase

class Filter(TableBase):
    def __init__(self,table_name):
        self.conditions = []
        self.joins = []
        
        self.result = None
        self.query = None
        
    def limit(self,value):
        pass
    
    def where(self,where):
        pass


    def __str__(self):
        return f"{self.result}"