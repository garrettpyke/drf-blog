from rest_framework import serializers
from ..models import Blog

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('id', 'title', 'content', 'category', 'author', 'updated_at')
        # fields = '__all__'