from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.blog import BlogSerializer
from ..models.blog import Blog
from ..serializers.comment import CommentSerializer
from ..models.comment import Comment
from ..serializers.user import UserSerializer
from ..models.user import MyUser as User
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

# todo: return related urls & data from views to make fully RESTful

def teapot_success_response(self):
    content = {'your request was successful, but you should know that I\'m a little teapot and may be short and stout.'}
    return Response(content, status=status.HTTP_200_OK)

class BlogsView(APIView):
    def get(self, request):
        # blogs = Blog.objects.filter(author=request.user.id) # decided to remove the filter as I want any user to see all blogs
        blogs = Blog.objects.all()
        user = get_object_or_404(User, pk=request.user.id)
        blog_data = BlogSerializer(blogs, many=True).data
        user_data = UserSerializer(user, many=False).data
        data = [blog_data, user_data]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data['author'] = request.user.id
        blog = BlogSerializer(data=request.data)
        if blog.is_valid():
            blog.save()
            return Response(blog.data, status=status.HTTP_201_CREATED)
        else:
            return Response(blog.errors, status=status.HTTP_400_BAD_REQUEST)
        
class BlogView(APIView):
    def get(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        if request.user != blog.author:
            raise PermissionDenied('Unauthorized, you do not own this blog')
        else:  
            data = BlogSerializer(blog).data
            return Response(data)
        # todo: Need to return all comments, but will need a separate serializer to attach to each blog.

    def delete(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        if request.user != blog.author:
            raise PermissionDenied('Unauthorized, you do not own this blog')
        else:  
            blog.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
    def patch(self, request, pk):
        """
        No PUT method is necessary. This PATCH works for both partial and complete updates.
        """
        blog = get_object_or_404(Blog, pk=pk)
        request.data['author'] = request.user.id
        updated_blog = BlogSerializer(blog, data=request.data, partial=True)  # partial=True argument allows request to omit the content field. (title field is set to required in models/blog.py)
        if request.user != blog.author:
            raise PermissionDenied('Unauthorized, you do not own this blog')
        else:
            if updated_blog.is_valid():
                updated_blog.save()
                return Response(updated_blog.data)
            else:
                return Response(updated_blog.errors, status=status.HTTP_400_BAD_REQUEST)
