from rest_framework import viewsets,generics
from ..models import Country
from ..serializers import countrySerializer,CountrySerializer1
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView






class CountryView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer1

    def list(self, request):
            filter_kwargs = {}
            print("kojhbv")

            for key, value in request.query_params.items():
                filter_kwargs[key] = value

            # if not filter_kwargs:
            #     return super().list(request)

            try:
                queryset = Country.objects.filter(**filter_kwargs)
                
                if not queryset.exists():
                    return Response({
                        'message': 'Data not found',
                        'status': 404
                    })

                serialized_data = CountrySerializer1(queryset, many=True)
                return Response(serialized_data.data)

            except Country.DoesNotExist:
                return Response({
                    'message': 'Objects not found',
                    'status': 404
                })