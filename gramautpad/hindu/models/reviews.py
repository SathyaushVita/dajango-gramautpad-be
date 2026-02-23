import uuid
from django.db import models
from .product import Product 
from .user import User  

class Review(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False)
    review_text = models.TextField(db_column='review_text')
    rating = models.IntegerField(db_column='rating')
    product = models.ForeignKey(Product, db_column='product_id', on_delete=models.CASCADE)
    user = models.ForeignKey(User, db_column='user_id', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(db_column='created_at', auto_now_add=True)


    class Meta:
        db_table = 'reviews'

    def __str__(self):
        return f"Review by {self.user} for {self.product.name} (Rating: {self.rating})"
