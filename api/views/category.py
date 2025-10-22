# from django.shortcuts import get_object_or_404
# from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.exceptions import PermissionDenied
from rest_framework import status, generics
# from rest_framework.authtoken.models import Token
from ..models.category import Category
from ..serializers.category import CategorySerializer

class CategoryView(generics.ListAPIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response({'categories': serializer.data})
