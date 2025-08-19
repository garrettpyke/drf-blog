from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum
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

def vote_not_accepted_response(self, content=None):
    content = {"vote not accepted": 'vote already exists'} if content is None else content
    return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

class BlogVotesView(APIView):
    def get_existing_vote(self, blog_votes_view, blog):
        # vote_type_sum = Vote.objects.filter(blog=blog, voter_id=self.request.user.id).aggregate(Sum("vote_type")) # {'vote_type__sum': 3}
        # vote_count = Vote.objects.filter(blog=blog, voter_id=self.request.user.id).aggregate(Count("vote_type")) # {'vote_type__count': 2}
        if Vote.objects.filter(blog=blog, voter=self.request.user.id).exists():
            return Vote.objects.filter(blog=blog, voter=self.request.user.id).values("vote_type", "voted_at").latest("voted_at")
        return 0
    
    def post(self, request, pk):
        """
        Allows each user to add or modify 1 vote per Blog
        """ 
        blog = get_object_or_404(Blog, pk=pk)
        existing_vote = self.get_existing_vote(self, blog)
        print(existing_vote)
        if existing_vote['vote_type'] == request.data['vote_type']:
            return vote_not_accepted_response(self)
        request.data['voter'] = request.user.id
        request.data['blog'] = blog.id
        vote = VoteSerializer(data=request.data)
        if not vote.is_valid():
            return vote_not_accepted_response(self, content={"vote not accepted": "bad request"})
        vote.save()
        return Response(vote.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, pk):
        # blog = get_object_or_404(Blog, pk=pk)
        # blog = get_object_or_404(Blog.objects.filter(pk=pk)) # Blog | None
        blog = Blog.objects.filter(pk=pk).first() # Blog | None
        print(blog)
        if blog:
            votes = blog.vote_set.all() # todo: Works! Filter this by request.user.id
            print(votes) 
            return Response({"blog found": ""}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        return Response({"blog not found": ""}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        # vote = get_object_or_404(Vote.objects.filter(blog=blog, voter=request.user.id))
        # print(vote)
        # todo - verify vote belongs to user!
        