from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from ..models.comment import Comment
from ..serializers.comment import CommentSerializer
from ..models.blog import Blog

def political_no_content_response(self):
    content = {"Message 1": 'As politicians say, no comment!', "Message 2": ""}
    return Response(content, status=status.HTTP_204_NO_CONTENT)

class CommentsView(APIView):
    def get(self, request, *args, **kwargs):
        comments = Comment.objects.filter(author=request.user)
        if data := CommentSerializer(comments, many=True).data:
            return Response(data, status=status.HTTP_200_OK)
        return Response('As politicians say, no comment!', status=status.HTTP_204_NO_CONTENT)
    
    def post(self, request, blog_id):
        request.data['author'] = request.user.id
        blog = get_object_or_404(Blog, id=blog_id)
        if not blog:
            raise PermissionDenied('No such blog exists or blog data invalid')
        request.data['blog'] = blog.id
        comment = CommentSerializer(data=request.data)
        if not comment.is_valid():
            return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)
        comment.save()
        return Response(comment.data, status=status.HTTP_201_CREATED)
            
class CommentView(APIView):
    def get(self, request, blog_id):
        blog = get_object_or_404(Blog, id=blog_id)
        comments = Comment.objects.filter(blog=blog)
        if data := CommentSerializer(comments, many=True).data:
            return Response(data)
        return political_no_content_response(self)
    
    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if request.user != comment.author:
            raise PermissionDenied('Unauthorized, you do not own this comment')
        comment.delete()
        return Response('Comment deleted', status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, pk):
        try:
            comment = Comment.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({"error": "Comment doesn't exist for you"}, status=status.HTTP_404_NOT_FOUND)
        if request.user != comment.author:
            raise PermissionDenied('Unauthorized, you do not own this comment')
        request.data['blog'] = comment.blog.id
        request.data['author'] = request.user.id
        data = CommentSerializer(comment, data=request.data, partial=False)
        if not data.is_valid():
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
        data.save()
        return Response(data.data, status=status.HTTP_202_ACCEPTED)