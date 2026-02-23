from django.db import models
import uuid
from .sub_category import SubCategory 



class Product(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False)
    name = models.CharField(db_column='name', max_length=45) 
    desc = models.CharField(db_column='desc', max_length=10000)
    sub_category = models.ForeignKey(SubCategory, db_column='sub_category_id', on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    quantity = models.IntegerField()
    status = models.CharField(max_length=20) 
    weight = models.CharField(max_length=100)  
    image = models.TextField( blank=True, null=True)  

   
    class Meta:
        managed = False
        db_table = 'product'
