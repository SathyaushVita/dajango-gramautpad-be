import uuid
from django.db import models
from .product import Product
from .user import User 


class Wishlist(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False)
    product = models.ForeignKey(Product, db_column='product_id', on_delete=models.CASCADE, blank=True, null=True, related_name='wishlists')
    added_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE, null=True, blank=True, related_name='wishlists')

    class Meta:
        db_table = 'wishlist'
        unique_together = ('product', 'user')  # Each user can only wishlist a product once
