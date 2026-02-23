from rest_framework import serializers
from ..models import MainCategory




class MainCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = MainCategory
        fields = "__all__"