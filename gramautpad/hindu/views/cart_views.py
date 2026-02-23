from rest_framework import generics, permissions
from rest_framework.response import Response
from ..models import Cart, Product
from ..serializers import CartSerializer

# List all items in the cart or add a new item
class CartListCreateView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure user is authenticated

    def perform_create(self, serializer):
        # Automatically get the authenticated user from the request
        user = self.request.user
        serializer.save(user=user)

# Retrieve, update, or delete a specific cart item
class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure user is authenticated
    lookup_field = '_id'
