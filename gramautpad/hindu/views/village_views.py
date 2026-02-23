from ..serializers import *
from ..models import Village,Block
from rest_framework import generics, status

from rest_framework import viewsets,status
from rest_framework .response import Response
from ..utils import CustomPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from ..utils import save_image_to_azure,send_email, send_mail
from django.conf import settings
from django.utils import timezone



class VillageView(viewsets.ModelViewSet):
    queryset = Village.objects.all()
    serializer_class = VillageSerializer
    pagination_class = CustomPagination
    # permission_classes = []
    
    # def get_permissions(self):
    #     if self.request.method in ['POST', 'PUT', ]:
    #         return [IsAuthenticated()]
    #     return super().get_permissions()


    # def get_queryset(self):
    #     return Village.objects.filter(status='ACTIVE')


    def list(self, request):
        filter_kwargs = {}

        for key, value in request.query_params.items():
            filter_kwargs[key] = value

        # if not filter_kwargs:
        #     return super().list(request)

        try:
            queryset = Village.objects.filter(**filter_kwargs)
            
            if not queryset.exists():
                return Response({
                    'message': 'Data not found',
                    'status': 404
                })

            serialized_data = VillageSerializer(queryset, many=True)
            return Response(serialized_data.data)

        except Village.DoesNotExist:
            return Response({
                'message': 'Objects not found',
                'status': 404
            })
        
    def create(self, request, *args, **kwargs):
        try:
            # Extract image_location from request data
            image_location = request.data.get('image_location')
            
            # Add the image_location back to the request data
            request.data['image_location'] = "null"

            # Serialize data and save
            print("sqwfrgth")
            serializer = VillageSerializer2(data=request.data)
            serializer.is_valid(raise_exception=True)
            print("asdfghj")
            serializer.save()
            print("qwertyu")
            
            if image_location and image_location != "null":
                saved_location = save_image_to_azure(image_location, serializer.instance._id, serializer.instance.name, "village")
                if saved_location:
                    serializer.instance.image_location = saved_location
                    serializer.instance.save()

            # Capture the current time
            created_at = timezone.now()

            # Send email to EMAIL_HOST_USER
            # send_mail(
            #     'New Temple Added',
            #     f'User ID: {request.user._id}\n'
            #     f'Full Name: {request.user.name()}\n'
            #     f'Created Time: {created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
            #     f'Temple ID: {serializer.instance._id}\n'
            #     f'Temple Name: {serializer.instance.name}',
            #     settings.EMAIL_HOST_USER,
            #     [settings.EMAIL_HOST_USER],
            #     fail_silently=False,
            # )

            return Response({
                "message": "success",
                "result": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


        
        





class villages_By_Block(generics.GenericAPIView):
    serializer_class = VillageSerializer

    def get(self, request, block):
        try:
            # Fetch the villages using the provided block_id
            villages = Village.objects.filter(block=block)

            if not villages.exists():
                return Response({
                    "message": "No villages found for this block",
                    "status": 404
                }, status=status.HTTP_404_NOT_FOUND)

            # Serialize the data
            serialized_data = VillageSerializer(villages, many=True)
            village_count = villages.count()

            return Response({
                "village_count": village_count,
                "villages": serialized_data.data
            }, status=status.HTTP_200_OK)

        except Block.DoesNotExist:
            return Response({
                'message': 'Block not found',
                'status': 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'message': str(e),
                'status': 500
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)