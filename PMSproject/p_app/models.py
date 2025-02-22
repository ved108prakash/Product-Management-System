from django.db import models

# Create your models here.
class Product(models.Model):
    pid=models.IntegerField(primary_key=True)
    pname=models.CharField(max_length=30)
    price=models.IntegerField()
    quantity=models.IntegerField()
    category=models.CharField(max_length=30)
    orderdate=models.DateTimeField()

    def __str__(self):
        return self.pname
