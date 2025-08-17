from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from ..models.blog import Blog
# from ..serializers.blog import BlogSerializer
from ..models.user import MyUser as User
# from ..serializers.user import UserSerializer
from ..models.vote import Vote
from ..serializers.vote import VoteSerializer

class BlogVotesView(APIView): # todo: make sure each user can only cast 1 vote per blog
    def post(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        request.data['voter'] = request.user.id
        request.data['blog'] = blog.id
        request.data['vote_type'] =  Vote.LIKE
        vote = VoteSerializer(data=request.data)
        if not vote.is_valid():
            return Response({"error": "vote didn't work!"}, status=status.HTTP_400_BAD_REQUEST)
        vote.save()
        return Response(vote.data, status=status.HTTP_201_CREATED)