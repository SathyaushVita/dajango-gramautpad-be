from rest_framework import viewsets, generics
from ..models import SubCategory,Product
from ..serializers.sub_category_serializer import SubCategorySerializer
from rest_framework.decorators import action
from ..serializers import ProductSerializer
from rest_framework.response import Response




class SubCategoryView(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer




    def list(self, request):
        filter_kwargs = {}
        print("abcd")

        for key, value in request.query_params.items():
            filter_kwargs[key] = value

        # if not filter_kwargs:
        #     return super().list(request)

        try:
            queryset = SubCategory.objects.filter(**filter_kwargs)
            
            if not queryset.exists():
                return Response({
                    'message': 'Data not found',
                    'status': 404
                })

            serialized_data = SubCategorySerializer(queryset, many=True)
            return Response(serialized_data.data)

        except SubCategory.DoesNotExist:
            return Response({
                'message': 'Objects not found',
                'status': 404
            })