from ..models import Wishlist
from ..serializers import WishlistSerializer,WishlistSerializer1
from rest_framework import viewsets
from rest_framework .response import Response
from rest_framework import generics,status



class WishlistViews(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer





    def create(self, request, *args, **kwargs):
        serializer = WishlistSerializer1(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': 'Invalid data',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)







    def list(self, request):
            filter_kwargs = {}

            for key, value in request.query_params.items():
                filter_kwargs[key] = value

            # if not filter_kwargs:
            #     return super().list(request)

            try:
                queryset = Wishlist.objects.filter(**filter_kwargs)
                
                if not queryset.exists():
                    return Response({
                        'message': 'Data not found',
                        'status': 404
                    })

                serialized_data = WishlistSerializer(queryset, many=True)
                return Response(serialized_data.data)

            except Wishlist.DoesNotExist:
                return Response({
                    'message': 'Objects not found',
                    'status': 404
                })






    