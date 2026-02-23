from rest_framework import serializers
from ..models import User
from ..utils import image_path_to_binary,video_path_to_binary
from .seller_product_serializer import SellerSerializer


class Loginserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class Verifyserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "verification_otp"]



class RegisterSerializer1(serializers.ModelSerializer):
    sellers  = SellerSerializer(many=True, read_only=True) 

    

    class Meta:
        model = User
        fields = ["id","full_name","gender","age","contact_number","email","address","address","id_type","id_number","id_proof","object_id","stakeholder_type","highest_education_qualification","is_working_professional","years_of_work_experience","resume","pincode","surname","sellers"]
        def get_product_certification(self, obj):
         return image_path_to_binary(obj.product_certification) if obj.product_certification else None

        def get_product_image(self, obj):
            return image_path_to_binary(obj.product_image) if obj.product_image else None

        def get_product_video(self, obj):
            return video_path_to_binary(obj.product_video) if obj.product_video else None
