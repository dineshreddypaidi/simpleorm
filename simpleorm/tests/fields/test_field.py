import pytest

from simpleorm.fields.base import Field
from simpleorm.fields import *

def test_integer_field_type():
    field = IntegerField()
    assert field.py_type is int

def test_string_field_type():
    field = StringField()
    assert field.py_type is str

def test_float_field_type():
    field = FloatField()
    assert field.py_type is float

def test_text_field_type():
    field = TextField()
    assert field.sql_type == "TEXT"


def test_boolean_field_type():
    field = BooleanField()
    assert field.py_type is bool

def test_date_field_type():
    field = DateField()
    assert field.sql_type == "DATE"

def test_datetime_field_type():
    field = DateTimeField()
    assert field.sql_type == "TIMESTAMP"

def test_field_abstract_instantiation():
    with pytest.raises(TypeError):
        Field(int, "INTEGER")

def test_to_sql():
    sql = IntegerField(unique=True)
    sql = sql.to_sql("id")
    assert isinstance(sql,dict)