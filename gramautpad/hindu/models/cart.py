

import uuid
from django.db import models
from .product import Product
from .user import User

class Cart(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False)
    user = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, db_column='product_id', on_delete=models.CASCADE)
    quantity = models.IntegerField(db_column='quantity', default=1)
    added_at = models.DateTimeField(db_column='added_at', auto_now_add=True)

    class Meta:
        db_table = 'cart'

    def __str__(self):
        return f"{self.product.name} (x{self.quantity}) added by {self.user.username}"
