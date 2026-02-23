from rest_framework import viewsets, generics
from ..models import Product
from ..serializers.product_serializer import ProductSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from ..utils import CustomPagination



class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer






    def list(self, request):
        filter_kwargs = {}
        print("abcd")

        for key, value in request.query_params.items():
            filter_kwargs[key] = value

        # if not filter_kwargs:
        #     return super().list(request)

        try:
            queryset = Product.objects.filter(**filter_kwargs)
            
            if not queryset.exists():
                return Response({
                    'message': 'Data not found',
                    'status': 404
                })

            serialized_data = ProductSerializer(queryset, many=True)
            return Response(serialized_data.data)

        except Product.DoesNotExist:
            return Response({
                'message': 'Objects not found',
                'status': 404
            })
