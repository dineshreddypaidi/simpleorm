from .base import Field

class IntegerField(Field):
    def __init__(self, **kwargs):
        super().__init__(int,"INTEGER", **kwargs)
        
    def validate(self):
        pass
class StringField(Field):
    def __init__(self, max_length=255, **kwargs):
        sql_type = f"VARCHAR({max_length})"
        self.max_length = max_length
        super().__init__(str, sql_type, **kwargs)

    def validate(self):
        self._validate_flags_for_type(allow_pk=False, allow_unique=False, allow_fk=False)
        
class FloatField(Field):
    def __init__(self,**kwargs):
        super().__init__(float, "FLOAT", **kwargs)
          
    def validate(self):
        if self.auto_increment:
            raise ValueError("float cannot be primary key and can't auto_increment")
class TextField(Field):
    def __init__(self,**kwargs):
        super().__init__(str, "TEXT", **kwargs)
        
    def validate(self):
        self._validate_flags_for_type(allow_pk=False, allow_unique=False, allow_fk=False)
        
class BooleanField(Field):
    def __init__(self,**kwargs):
        super().__init__(bool, "BOOLEAN",**kwargs)
  
    def validate(self):
        self._validate_flags_for_type(allow_pk=False, allow_unique=False, allow_fk=False)

class DateField(Field):
    def __init__(self, auto=False, **kwargs):
        self.auto = auto
        super().__init__(str, "DATE", **kwargs)

    def validate(self):
        self._validate_flags_for_type(allow_pk=False, allow_unique=False, allow_fk=False)

class DateTimeField(Field):
    def __init__(self, auto=False, **kwargs):
        self.auto = auto
        super().__init__(str, "TIMESTAMP",**kwargs)

    def validate(self):
        self._validate_flags_for_type(allow_pk=False, allow_unique=False, allow_fk=False)