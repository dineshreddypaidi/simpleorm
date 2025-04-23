class BaseConnector():
    def __init__(self,config : dict):
        self.config = config
        self.conn = None
        
    def connect(self):
        if self.conn is None:
            self.get_connection()
        return self.conn
    
    def get_cursor(self):
        if not self.conn is None:
            return self.conn.cursor()
        else:
            raise ConnectionError("database not connected")