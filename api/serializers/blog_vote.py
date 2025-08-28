from rest_framework import serializers
from ..models import Blog
from ..models import Vote

class NestedVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
        # fields = ('vote_type', 'blog', 'voter', 'voted_at')

class BlogVoteSerializer(serializers.ModelSerializer):
    votes = NestedVoteSerializer(many=True, read_only=True)
    
    class Meta:
        model = Blog
        fields = ['title', 'content', 'category', 'author', 'updated_at', 'votes']