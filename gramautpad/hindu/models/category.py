from django.db import models
import uuid
from .main_category import MainCategory


class Category(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False)
    name = models.CharField(db_column='name', max_length=45, blank=True, null=True) 
    desc = models.CharField(db_column='desc', max_length=250, blank=True, null=True)
    main_category = models.ForeignKey(MainCategory, db_column='main_category_id', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image= models.TextField(null=True,blank=True)

    class Meta:
        managed = False
        db_table = 'category'