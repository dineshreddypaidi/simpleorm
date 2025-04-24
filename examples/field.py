import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from simpleorm.fields import *
        
print(IntegerField(primary_key=True).schema("id"))

print(StringField().schema("id"))

print(FloatField(default=10.2).schema("id"))

print(TextField().schema("id"))

print(BooleanField().schema("id"))

print(DateField(auto=True).schema("id"))

print(DateTimeField(auto=True).schema("id"))