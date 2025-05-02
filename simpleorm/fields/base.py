from abc import ABC, abstractmethod

class Field(ABC):
    def __init__(self, py_type, sql_type, null=False, primary_key=False, unique=False,
                 foreign_key=None, auto_increment=False, default=None):
                                        
        self.py_type = py_type
        self.sql_type = sql_type
        self.null = null
        self.primary_key = primary_key
        self.unique = unique
        self.foreign_key = foreign_key
        self.auto_increment = auto_increment
        self.default = default
        
        self.__set_constraints()
        self.__validate_constraints()
        
    def __set_constraints(self):
        if self.primary_key:
            self.auto_increment = True
            self.unique = True
            self.null = False
            
        if self.auto_increment:
            self.primary_key = True
            self.unique = True
            self.null = False
    
    def __validate_constraints(self):
        if self.auto_increment and not self.primary_key:
            raise ValueError("AUTOINCREMENT is only allowed with primary key fields")
        if self.primary_key and self.null:
            raise ValueError("Primary key field cannot be nullable")
        if self.default is not None and not isinstance(self.default, self.py_type):
            raise TypeError(f"Default value must be of type {self.py_type.__name__}")
        if self.primary_key and self.auto_increment and self.default is not None:
            raise ValueError("When primary and auto_increment are set, default value cannot be specified")
        if self.primary_key and not self.unique:
            raise ValueError("Primary key must be unique")
        if self.foreign_key:
            ref_table, ref_col = self.foreign_key.split("(")
            ref_col = ref_col.rstrip(")")
            if not ref_table or not ref_col:
                raise ValueError(f"Invalid foreign key format. Expected format: 'table_name(column_name)'")
        if self.unique and self.null:
            raise ValueError("A field with 'unique' constraint cannot be nullable")
        if self.foreign_key and self.unique:
            raise ValueError("A foreign key field cannot be unique")
        if self.auto_increment and self.foreign_key:
            raise ValueError("Auto increment field cannot be a foreign key")
        if self.primary_key and self.default is not None:
            raise ValueError("Primary key fields should not have a default value unless auto_increment is used")
        if self.foreign_key and self.null:
            raise ValueError("Foreign key field cannot be nullable")
    
    def _validate_flags_for_type(self, allow_pk=False, allow_unique=False, allow_fk=False):
        if not allow_pk and (self.primary_key or self.auto_increment):
            raise ValueError(f"{self.sql_type} cannot be primary key or auto_increment")
        if not allow_unique and self.unique:
            raise ValueError(f"{self.sql_type} cannot be unique")
        if not allow_fk and self.foreign_key:
            raise ValueError(f"{self.sql_type} cannot be a foreign key")
        
    @abstractmethod
    def validate(self):
        pass

    def __str__(self):
        return f"{self.__class__.__name__}({self.sql_type})"
    
    def to_sql(self, column_name):
        self.validate()
        
        parts = {
            "column_name" : column_name,
            "sql_type" :  self.sql_type,
        }
        
        if self.null:
            parts["not_null"] = self.null
        if self.primary_key:
            parts["is_primary"] = self.primary_key
        if self.unique:
            parts["is_unique"] = self.unique
        if self.foreign_key:
            ref_table, ref_col = self.foreign_key.split("(")
            ref_col = ref_col.rstrip(")")
            parts["foreign_key"] = f"REFERENCES {ref_table}({ref_col})"
        if self.auto_increment:
            parts["auto_increment"] = ("AUTOINCREMENT")
        if self.default is not None:
            default_val = f"'{self.default}'" if isinstance(self.default, str) else str(self.default)
            parts["default"] = (f"DEFAULT {default_val}")
            
        if hasattr(self, "auto") and self.auto:
            parts["is_auto"] = self.auto
    
        return parts