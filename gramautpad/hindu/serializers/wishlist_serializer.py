from rest_framework import serializers
from ..models import Wishlist
from ..utils import image_path_to_binary



class WishlistSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(read_only=True)

    # def get_product(self, instance):
    #     product = instance.product
    #     if product:
    #         return {
    #             "_id": str(product._id),
    #             "name": product.name,
    #             "image": product.image
    #         }


    def get_product(self,instance):
        product = instance.product
        def get_image(product):
                filename = product.image
                if filename:
                    format= image_path_to_binary(filename)
                    # print(format,"******************")
                    return format
                return[]
        if product:
            return{
                "_id":product._id,
                "name":product.name,
                "image":get_image(product),
            }

    class Meta:
        model = Wishlist
        fields = "__all__"

class WishlistSerializer1(serializers.ModelSerializer):


    class Meta:
        model = Wishlist
        fields = "__all__"



