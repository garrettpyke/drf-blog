from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from ..models.blog import Blog
from ..serializers.blog_vote import BlogVoteSerializer
from ..models.comment import Comment
from ..serializers.comment import CommentSerializer
from ..models.vote import Vote
from ..serializers.vote import VoteSerializer

def vote_not_accepted_response(self, content=None):
    content = {"vote not accepted": 'you have an existing vote (limit 1 per customer)'} if content is None else content
    return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

class BlogVotesView(APIView):
    def get_existing_vote(self, blog_votes_view, blog):
        # vote_type_sum = Vote.objects.filter(blog=blog, voter_id=self.request.user.id).aggregate(Sum("vote_type")) # {'vote_type__sum': 3}
        # vote_count = Vote.objects.filter(blog=blog, voter_id=self.request.user.id).aggregate(Count("vote_type")) # {'vote_type__count': 2}
        if Vote.objects.filter(blog=blog, voter=self.request.user.id).exists():
            return Vote.objects.filter(blog=blog, voter=self.request.user.id).get()
        return None
    
    def get(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        blog_votes = BlogVoteSerializer(blog).data
        comments = Comment.objects.filter(blog_id=blog.id).all()
        blog_comments = CommentSerializer(comments, many=True).data or []
        # data = [blog_votes, blog_comments]
        data = [blog_votes, {'comments': blog_comments}]
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        """
        Allows each user to add 1 vote per Blog
        """ 
        blog = get_object_or_404(Blog, pk=pk)
        if self.get_existing_vote(self, blog):
            return vote_not_accepted_response(self)
        request.data['voter'] = request.user.id
        request.data['blog'] = blog.id
        vote = VoteSerializer(data=request.data)
        if not vote.is_valid():
            message = {"vote not accepted": vote.errors}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        vote.save()
        return Response(vote.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, pk):
        if blog := Blog.objects.filter(pk=pk).first(): # Blog | None
            if vote := self.get_existing_vote(self, blog):
                vote.delete()
                return Response({"vote deleted": ""}, status=status.HTTP_204_NO_CONTENT)
            return Response({"vote not found": ""}, status=status.HTTP_404_NOT_FOUND) 
        return Response({"blog not found": ""}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        if blog := Blog.objects.filter(pk=pk).first(): # Blog | None
            if request.data['vote_type'] in Vote.VOTE_TYPE_CHOICES:
                Vote.objects.filter(blog=blog, voter=self.request.user.id).update(vote_type=request.data['vote_type'])
                return Response({"vote updated": ""}, status=status.HTTP_202_ACCEPTED) 
            return Response({"invalid vote": ""}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"blog not found": ""}, status=status.HTTP_404_NOT_FOUND)