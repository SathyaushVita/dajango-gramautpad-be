from rest_framework import serializers
from ..models import Village
from ..utils import image_path_to_binary


class VillageSerializer(serializers.ModelSerializer):


    class Meta:
        model = Village
        fields = "__all__"


class VillageSerializer1(serializers.ModelSerializer):

    image_location = serializers.SerializerMethodField()
    def get_image_location(self, instance):

            filename = instance.image_location
            if filename:
                format= image_path_to_binary(filename)
                # print(format,"******************")
                return format
            return None
    class Meta:
        model = Village
        fields = "__all__"

class VillageSerializer2(serializers.ModelSerializer):

    
    class Meta:
        model = Village
        fields = "__all__"


