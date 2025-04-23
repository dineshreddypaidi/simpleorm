from abc import ABC, abstractmethod
class BaseConnector(ABC):
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

    def commit(self):
        if not self.conn is None:
            self.conn.commit()
        else:
            raise ConnectionError("database not connected")

    @abstractmethod
    def show_tables(self):
        pass

    # @abstractmethod
    # def create_table(self):
    #     pass

    @abstractmethod
    def drop_table(self):
        pass
    