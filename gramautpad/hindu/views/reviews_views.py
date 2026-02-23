from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import Review,Product,User
from ..serializers import ReviewSerializer
from rest_framework.permissions import IsAuthenticated

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()  
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated] 

    def create(self, request, *args, **kwargs):
        """Override create method to add user automatically"""
        user = request.user
        # Automatically associate the logged-in user if not provided
        if 'user' not in request.data:
            request.data['user'] = user.id
        return super().create(request, *args, **kwargs)


    @action(detail=True, methods=['get'])
    def product_reviews(self, request, pk=None):
        """Retrieve all reviews for a specific product"""
        product = Product.objects.get(pk=pk)
        reviews = Review.objects.filter(product=product)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def user_reviews(self, request, pk=None):
        """Retrieve all reviews by a specific user"""
        user = User.objects.get(pk=pk)
        reviews = Review.objects.filter(user=user)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
