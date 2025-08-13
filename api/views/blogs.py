from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from ..serializers.blog import BlogSerializer
from ..models.blog import Blog
from ..serializers.comment import CommentSerializer
from ..models.comment import Comment
from ..serializers.user import UserSerializer
from ..models.user import MyUser as User

# todo: return related urls & data from views to make fully RESTful

def teapot_no_content_response(self):
    content = {"204 -> 418 I'm an EMPTY teapot": "Any attempt to brew coffee with a teapot should result in the error code '418 I'm a teapot'. The resulting entity body MAY be short and stout."}
    return Response(content, status=status.HTTP_204_NO_CONTENT)

class BlogsView(APIView):
    def get(self, request):
        blogs = Blog.objects.all()
        user = get_object_or_404(User, pk=request.user.id)
        blog_data = BlogSerializer(blogs, many=True).data or 'Wow, such empty.'
        user_data = UserSerializer(user, many=False).data
        data = [blog_data, user_data] # experimenting with my responses here regarding the todo on l.13
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data['author'] = request.user.id
        blog = BlogSerializer(data=request.data)
        if not blog.is_valid():
            return Response(blog.errors, status=status.HTTP_400_BAD_REQUEST)
        blog.save()
        return Response(blog.data, status=status.HTTP_201_CREATED)

class BlogsAuthorView(APIView):
    def get(self, request, id): # todo: Each post should have another json file containing {[url], [blog detail url]}
        blogs = Blog.objects.filter(author=id)
        if data := BlogSerializer(blogs, many=True).data:
            return Response(data, status=status.HTTP_200_OK)
        else:
            return teapot_no_content_response(self)

class BlogView(APIView):
    def get(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        if request.user != blog.author:
            raise PermissionDenied('Unauthorized, you do not own this blog')
        if data := BlogSerializer(blog).data:
            return Response(data, status=status.HTTP_200_OK)
        # todo: Need to return all comments, but will need a separate serializer to attach to each blog.

    def delete(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        if request.user == blog.author:
            blog.delete()
            return Response('Blog deleted', status=status.HTTP_204_NO_CONTENT)
        raise PermissionDenied('Unauthorized, you do not own this blog')
        
    def patch(self, request, pk):
        """
        No PUT method is necessary. This PATCH works for both partial and complete updates.
        partial=True argument allows request to omit the content field, tho title field is set to required in models/blog.py.
        """
        blog = get_object_or_404(Blog, pk=pk)
        request.data['author'] = request.user.id
        if request.user != blog.author:
            raise PermissionDenied('Unauthorized, you do not own this blog')
        updated_blog = BlogSerializer(blog, data=request.data, partial=True)
        if not updated_blog.is_valid():
            return Response(updated_blog.errors, status=status.HTTP_400_BAD_REQUEST)
        updated_blog.save()
        return Response(updated_blog.data, status=status.HTTP_202_ACCEPTED)
