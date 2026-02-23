from rest_framework import serializers
from ..models import Cart, Product, User

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['_id', 'user', 'product', 'quantity', 'added_at']
        read_only_fields = ['_id', 'added_at', 'user']  # Exclude 'user' from input and make it read-only

    def validate_product(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Invalid product ID.")
        return value

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value
