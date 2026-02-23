from rest_framework import viewsets, generics
from ..models import Category,SubCategory,Product
from ..serializers.category_serializer import CategorySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from ..utils import CustomPagination
from ..serializers import SubCategorySerializer,ProductSerializer
from rest_framework import viewsets, status




class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


    
    def list(self, request):
        filter_kwargs = {}
        print("abcd")

        for key, value in request.query_params.items():
            filter_kwargs[key] = value

        # if not filter_kwargs:
        #     return super().list(request)

        try:
            queryset = Category.objects.filter(**filter_kwargs)
            
            if not queryset.exists():
                return Response({
                    'message': 'Data not found',
                    'status': 404
                })

            serialized_data = CategorySerializer(queryset, many=True)
            return Response(serialized_data.data)

        except Category.DoesNotExist:
            return Response({
                'message': 'Objects not found',
                'status': 404
            })
        


    
    @action(detail=True, methods=['get'], url_path='products')
    def get_products(self, request, pk=None):
        # Retrieve the products associated with this category ID
        products = Product.objects.filter(sub_category__category_id=pk)
        
        # Serialize the product data
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)