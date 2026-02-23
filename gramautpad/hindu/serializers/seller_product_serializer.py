from rest_framework import serializers
from ..models import Seller

class SellerSerializer(serializers.ModelSerializer):
    seller_count = serializers.IntegerField(read_only=True)  
    buyer_count = serializers.IntegerField(read_only=True)   


    class Meta:
        model = Seller
        fields = "__all__"



