from rest_framework import serializers
from ..models import Product
from ..utils import image_path_to_binary




class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    def get_image(self, instance):

            filename = instance.image
            if filename:
                format= image_path_to_binary(filename)
                # print(format,"******************")
                return format
            return None


    class Meta:
        model = Product
        fields = "__all__"




class ProductSerializer1(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, instance):
        filename = instance.image
        if filename:
            format = image_path_to_binary(filename)
            return format
        return None

    class Meta:
        model = Product
        fields = ['_id', 'name', 'image']
