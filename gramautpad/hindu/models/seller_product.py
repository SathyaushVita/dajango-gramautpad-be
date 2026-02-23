import uuid
from django.db import models
from ..enums.geosite_enum import GeoSite
from .product import Product
from .village import Village
from .user import User 
from .sub_category import SubCategory 
from .category import Category 
from .main_category import MainCategory

from ..enums import *




class Seller(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False)
    product = models.ForeignKey(Product, db_column='product_id', on_delete=models.CASCADE, blank=True, null=True) 
    product_name = models.CharField(null=True,blank=True,max_length=100) 
    product_availability_time = models.DateTimeField(null=True, blank=True)
    product_quantity = models.CharField(null=True, blank=True,max_length=1000)
    product_quality = models.CharField(max_length=255, null=True, blank=True)
    product_certification = models.TextField(null=True, blank=True)
    expected_price =models.CharField(max_length=100,null=True,blank=True)
    product_image = models.TextField(null=True, blank=True)
    product_video = models.TextField(null=True, blank=True)
    geo_site = models.CharField(max_length=50, choices=[(e.name, e.value) for e in GeoSite], default=GeoSite.VILLAGE.value)
    object_id = models.ForeignKey(Village, db_column='object_id', on_delete=models.SET_NULL, null=True, blank=True, related_name='Seller') 
    user = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE, null=True, blank=True, related_name='sellers')
    sub_category = models.ForeignKey(SubCategory, db_column='sub_category_id', on_delete=models.CASCADE, null=True, blank=True)
    # category = models.ForeignKey(Category, db_column='category_id', on_delete=models.CASCADE, null=True, blank=True)  # Link to Category
    # main_category = models.ForeignKey(MainCategory, db_column='main_category_id', on_delete=models.CASCADE, null=True, blank=True)  # Link to MainCategory
    desc = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(db_column='status', max_length=50, choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value)



    








    class Meta:
        managed = False
        db_table = 'seller_product'
