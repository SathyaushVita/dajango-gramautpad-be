from rest_framework import viewsets
from ..models import Block,District
from ..serializers import BlockSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework .response import Response
from rest_framework import generics, status

class BlockView(viewsets.ModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer

    permission_classes = []
    
    def get_permissions(self):
        if self.request.method in [ 'POST', 'PUT']:
            return [IsAuthenticated()]
        return super().get_permissions()


    def list(self, request):
        filter_kwargs = {}

        for key, value in request.query_params.items():
            filter_kwargs[key] = value

        # if not filter_kwargs:
        #     return super().list(request)

        try:
            queryset = Block.objects.filter(**filter_kwargs)
            
            if not queryset.exists():
                return Response({
                    'message': 'Data not found',
                    'status': 404
                })

            serialized_data = BlockSerializer(queryset, many=True)
            return Response(serialized_data.data)

        except Block.DoesNotExist:
            return Response({
                'message': 'Objects not found',
                'status': 404
            })
        












class blocks_By_District(generics.GenericAPIView):
    serializer_class = BlockSerializer

    def get(self, request, district):
        try:
            blocks = Block.objects.filter(district=district)

            if not blocks.exists():
                return Response({
                    "message": "No blocks found for this district",
                    "status": 404
                }, status=status.HTTP_404_NOT_FOUND)

            # Serialize the data
            serialized_data = BlockSerializer(blocks, many=True)
            block_count = blocks.count()

            return Response({
                "block_count": block_count,
                "blocks": serialized_data.data
            }, status=status.HTTP_200_OK)

        except District.DoesNotExist:
            return Response({
                'message': 'District not found',
                'status': 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'message': str(e),
                'status': 500
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)