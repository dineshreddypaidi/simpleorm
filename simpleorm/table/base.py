from abc import ABC
import pandas as pd

class TableBase(ABC):
    def __init__(self,conn):
        self.conn = conn
        self.cursor = conn.cursor()
    

    def to_df(self):
        pass
    
    
    def to_csv(self):
        pass
    
    