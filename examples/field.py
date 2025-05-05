from simpleorm.fields import *
        
print(IntegerField(primary_key=True).to_sql("id"))

print(StringField().to_sql("id"))

print(FloatField(default=10.2).to_sql("id"))

print(TextField().to_sql("id"))

print(BooleanField().to_sql("id"))

print(DateField(auto=True).to_sql("id"))

print(DateTimeField(auto=True).to_sql("id"))