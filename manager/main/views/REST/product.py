from rest_framework import viewsets
from rest_framework import permissions
from main.serializers import ProductSerializer
from catalog.models import Product

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]