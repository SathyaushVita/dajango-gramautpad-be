from rest_framework import viewsets, generics
from ..models import MainCategory,Category
from ..serializers.main_category_serializer import MainCategorySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from ..utils import CustomPagination
from ..serializers import CategorySerializer



class MainCategoryView(viewsets.ModelViewSet):
    queryset = MainCategory.objects.all()
    serializer_class = MainCategorySerializer


    # @action(detail=True, methods=['get'])
    # def categories(self, request, pk=None):
    #     # Get the MainCategory by ID
    #     main_category = self.get_object()

    #     # Get all Categories related to this MainCategory
    #     categories = Category.objects.filter(main_category=main_category)

    #     # Serialize Categories
    #     serialized_data = CategorySerializer(categories, many=True).data

    #     # Return the list of Category data in the response
    #     return Response(serialized_data)