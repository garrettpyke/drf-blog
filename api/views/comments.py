from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.comment import CommentSerializer
from ..models.comment import Comment
from ..serializers.blog import Blog
from ..models.blog import Blog
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

class CommentsView(APIView):
    def get(self, request, *args, **kwargs):
        comments = Comment.objects.filter(author=request.user)
        data = CommentSerializer(comments, many=True).data
        return Response(data)
    
    def post(self, request, blog_id):
        request.data['author'] = request.user.id
        blog = get_object_or_404(Blog, id=blog_id)
        # if blog and blog.id == request.data.blog:
        if blog and request.data['blog'] == blog.id:
            comment = CommentSerializer(data=request.data)
            if comment.is_valid():
                comment.save()
                return Response(comment.data, status=status.HTTP_201_CREATED)
            else:
                return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied('No such blog exists or blog data invalid')
            
class CommentView(APIView):
    def get(self, request, blog_id):
        blog = get_object_or_404(Blog, id=blog_id)
        comments = Comment.objects.filter(blog=blog)
        data = CommentSerializer(comments, many=True).data
        return Response(data)
    
    # todo: test everything from here down
    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if request.user != comment.author:
            raise PermissionDenied('Unauthorized, you do not own this comment')
        else:  
            data = CommentSerializer(comment, data=request.data, partial=True)
            if data.is_valid():
                data.save()
                return Response(data.data)
            else:
                return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)