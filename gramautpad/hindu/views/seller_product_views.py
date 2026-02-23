
from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import Seller
from ..serializers import SellerSerializer
from ..utils import video_path_to_binary, save_video_to_azure, save_image_to_azure, image_path_to_binary
from django.db.models import Q
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated






class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


    # permission_classes = [IsAuthenticated]



    def create(self, request, *args, **kwargs):
        try:
            # Validate and save the seller instance
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            seller_instance = serializer.save()

            # Handle product_image
            product_image = request.data.get('product_image')
            if product_image:
                saved_product_image_path = save_image_to_azure(product_image, seller_instance._id, seller_instance.product_id, 'product_image')
                if saved_product_image_path:
                    seller_instance.product_image = saved_product_image_path
                    seller_instance.save()

            # Handle product_video
            product_video = request.data.get('product_video')
            if product_video:
                saved_product_video_path = save_video_to_azure(product_video, seller_instance._id, seller_instance.product_id, 'product_video')
                if saved_product_video_path:
                    seller_instance.product_video = saved_product_video_path
                    seller_instance.save()              

            # Save product_certification to folder like product_image
            product_certification = request.data.get('product_certification')
            if product_certification:
                saved_certification_path = save_image_to_azure(product_certification, seller_instance._id, seller_instance.product_id, 'product_certification')
                if saved_certification_path:
                    seller_instance.product_certification = saved_certification_path
                    seller_instance.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # print(f"Error during seller creation: {e}")
            return Response({"message": "An error occurred during seller creation.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






    def update(self, request, pk=None):
        try:
            # Get the existing seller instance
            instance = self.get_object()

            # Validate and update the seller instance
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            seller_instance = serializer.save()

            # Handle product_image update
            product_image = request.data.get('product_image')
            if product_image:
                saved_product_image_path = save_image_to_azure(product_image, seller_instance._id, seller_instance.product_id, 'product_image')
                if saved_product_image_path:
                    seller_instance.product_image = saved_product_image_path
                    seller_instance.save()

            # Handle product_video update
            product_video = request.data.get('product_video')
            if product_video:
                saved_product_video_path = save_video_to_azure(product_video, seller_instance._id, seller_instance.product_id, 'product_video', 'mp4')
                if saved_product_video_path:
                    seller_instance.product_video = saved_product_video_path
                    seller_instance.save()

            # Save product_certification to folder like product_image
            product_certification = request.data.get('product_certification')
            if product_certification:
                saved_certification_path = save_image_to_azure(product_certification, seller_instance._id, seller_instance.product_id, 'product_certification')
                if saved_certification_path:
                    seller_instance.product_certification = saved_certification_path
                    seller_instance.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Seller.DoesNotExist:
            return Response({'message': 'Seller not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # print(f"Error during seller update: {e}")
            return Response({"message": "An error occurred during seller update.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






    def list(self, request, *args, **kwargs):
        sellers = self.queryset
        serializer = self.get_serializer(sellers, many=True)

        for seller in serializer.data:
            # Convert product_image to base64
            if seller.get('product_image'):
                seller['product_image'] = image_path_to_binary(seller['product_image'])
            
            # Convert product_video to base64
            if seller.get('product_video'):
                print(f"Original product_video path: {seller['product_video']}")

                seller['product_video'] = video_path_to_binary(seller['product_video'])
                print(f"Converted product_video to binary: {seller['product_video']}")


            # Convert product_certification to base64
            if seller.get('product_certification'):
                seller['product_certification'] = image_path_to_binary(seller['product_certification'])

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            instance = self.get_object()
        except Seller.DoesNotExist:
            return Response({'message': 'Seller not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)

        # Convert file paths to base64
        data = serializer.data
        
        # Convert product_image to base64
        if data.get('product_image'):
            data['product_image'] = image_path_to_binary(data['product_image'])

        # Convert product_video to base64
        if data.get('product_video'):
            data['product_video'] = video_path_to_binary(data['product_video'])

        # Convert product_certification to base64
        if data.get('product_certification'):
            data['product_certification'] = image_path_to_binary(data['product_certification'])

        return Response(data, status=status.HTTP_200_OK)



















# from django.db.models import Q, Count
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.exceptions import ValidationError
# from rest_framework import generics
# from ..models import Seller, Product
# from ..serializers import SellerSerializer, ProductSerializer
# from ..utils import image_path_to_binary, video_path_to_binary

# class GetSellersByLocation(generics.ListAPIView):
#     serializer_class = SellerSerializer

#     def get_queryset(self):
#         input_value = self.request.query_params.get('input_value')
#         product_ids = self.request.query_params.get('product_id')

#         if not input_value and not product_ids:
#             raise ValidationError("Either 'input_value' (location) or 'product_id' (product) is required to retrieve sellers.")

#         # Parse product_ids into a list
#         product_id_list = product_ids.split(',') if product_ids else []

#         # Define location queries
#         country_query = Q(object_id__block__district__state__country__pk=input_value)
#         state_query = Q(object_id__block__district__state__pk=input_value)
#         district_query = Q(object_id__block__district__pk=input_value)
#         block_query = Q(object_id__block__pk=input_value)
#         village_query = Q(object_id__pk=input_value)

#         # Define product queries
#         product_query = Q(product__pk__in=product_id_list)

#         # Combine location and product queries
#         combined_query = Q()
#         if input_value:
#             combined_query |= country_query | state_query | district_query | block_query | village_query

#         if product_id_list:
#             combined_query &= product_query

#         # Query sellers based on combined query
#         queryset = Seller.objects.filter(combined_query).select_related(
#             'object_id__block__district__state__country',
#             'object_id__block__district__state',
#             'object_id__block__district',
#             'object_id__block',
#             'object_id',
#             'product'
#         ).annotate(seller_count=Count('product__seller', distinct=True))

#         if not queryset.exists() and product_id_list:
#             # If no sellers are found for the product_id, check the product model
#             # and return the product if it's found
#             queryset = Product.objects.filter(pk__in=product_id_list)

#         return queryset

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()

#         # If queryset contains products, use the ProductSerializer
#         if isinstance(queryset.first(), Product):
#             serializer = ProductSerializer(queryset, many=True)
#         else:
#             serializer = self.get_serializer(queryset, many=True)

#         # Convert file paths to binary format
#         for seller in serializer.data:
#             if seller.get('product_image'):
#                 seller['product_image'] = image_path_to_binary(seller['product_image'])
#             if seller.get('product_video'):
#                 seller['product_video'] = video_path_to_binary(seller['product_video'])
#             if seller.get('product_certification'):
#                 seller['product_certification'] = image_path_to_binary(seller['product_certification'])

#         return Response(serializer.data, status=status.HTTP_200_OK)










from django.db.models import Count, Q
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from rest_framework.response import Response
from ..models import Seller
from ..serializers import SellerSerializer
from ..utils import image_path_to_binary, video_path_to_binary 



class GetSellersByLocation(generics.ListAPIView):
    serializer_class = SellerSerializer

    def get_queryset(self):
        input_value = self.request.query_params.get('input_value')
        product_ids = self.request.query_params.get('product_id')

        if not input_value and not product_ids:
            raise ValidationError("Either 'input_value' (location) or 'product_id' (product) is required to retrieve sellers.")

        product_id_list = product_ids.split(',') if product_ids else []

        # Define location queries
        country_query = Q(object_id__block__district__state__country__pk=input_value)
        state_query = Q(object_id__block__district__state__pk=input_value)
        district_query = Q(object_id__block__district__pk=input_value)
        block_query = Q(object_id__block__pk=input_value)
        village_query = Q(object_id__pk=input_value)

        # Define product queries
        main_category_query = Q(product__sub_category__category_id__main_category__pk__in=product_id_list)
        category_id_query = Q(product__sub_category__category_id__pk__in=product_id_list)
        sub_category_query = Q(product__sub_category__pk__in=product_id_list)
        product_query = Q(product__pk__in=product_id_list)

        # Combine queries
        combined_query = Q()
        if input_value:
            combined_query |= country_query | state_query | district_query | block_query | village_query

        if product_id_list:
            combined_query &= main_category_query | category_id_query | sub_category_query | product_query

        # Filter sellers and count the number of distinct sellers per product
        queryset = Seller.objects.filter(combined_query).select_related(
            'object_id__block__district__state__country',
            'object_id__block__district__state',
            'object_id__block__district',
            'object_id__block',
            'object_id',
            'product__sub_category__category_id__main_category',
            'product__sub_category__category_id',
            'product__sub_category',
            'product'
        ).annotate(seller_count=Count('product__seller', distinct=True))

        if not queryset.exists() and input_value:
            queryset = Seller.objects.filter(object_id=input_value)
            if product_id_list:
                queryset = queryset.filter(product__pk__in=product_id_list).annotate(seller_count=Count('product__seller', distinct=True))

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Convert file paths to binary format
        for seller in serializer.data:
            if seller.get('product_image'):
                seller['product_image'] = image_path_to_binary(seller['product_image'])
            if seller.get('product_video'):
                seller['product_video'] = video_path_to_binary(seller['product_video'])
            if seller.get('product_certification'):
                seller['product_certification'] = image_path_to_binary(seller['product_certification'])

        return Response(serializer.data, status=status.HTTP_200_OK)
    



















from django.db.models import Q, Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from ..models import Seller, Product
from ..serializers import SellerSerializer, ProductSerializer
from ..utils import image_path_to_binary, video_path_to_binary

class GetproductsByLocation(generics.ListAPIView):
    serializer_class = SellerSerializer

    def get_queryset(self):
        input_value = self.request.query_params.get('input_value')
        product_ids = self.request.query_params.get('product_id')

        if not input_value and not product_ids:
            raise ValidationError("Either 'input_value' (location) or 'product_id' (product) is required to retrieve sellers.")

        # Parse product_ids into a list
        product_id_list = product_ids.split(',') if product_ids else []

        # Define location queries
        country_query = Q(object_id__block__district__state__country__pk=input_value)
        state_query = Q(object_id__block__district__state__pk=input_value)
        district_query = Q(object_id__block__district__pk=input_value)
        block_query = Q(object_id__block__pk=input_value)
        village_query = Q(object_id__pk=input_value)

        # Define product queries
        product_query = Q(product__pk__in=product_id_list)

        # Combine location and product queries
        combined_query = Q()
        if input_value:
            combined_query |= country_query | state_query | district_query | block_query | village_query

        if product_id_list:
            combined_query &= product_query

        # Query sellers based on combined query
        queryset = Seller.objects.filter(combined_query).select_related(
            'object_id__block__district__state__country',
            'object_id__block__district__state',
            'object_id__block__district',
            'object_id__block',
            'object_id',
            'product'
        ).annotate(seller_count=Count('product__seller', distinct=True))

        # If no sellers are found, query only the products
        if not queryset.exists():
            queryset = Product.objects.filter(pk__in=product_id_list) if product_id_list else Product.objects.none()

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # If the queryset contains products, use the ProductSerializer
        if queryset and isinstance(queryset.first(), Product):
            serializer = ProductSerializer(queryset, many=True)
        else:
            # Return an empty list if no products are found
            serializer = ProductSerializer(Product.objects.none(), many=True)

        # Convert file paths to binary format
        for product in serializer.data:
            if product.get('product_image'):
                product['product_image'] = image_path_to_binary(product['product_image'])
            if product.get('product_video'):
                product['product_video'] = video_path_to_binary(product['product_video'])
            if product.get('product_certification'):
                product['product_certification'] = image_path_to_binary(product['product_certification'])

        return Response(serializer.data, status=status.HTTP_200_OK)
