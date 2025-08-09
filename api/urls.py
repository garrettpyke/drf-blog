from django.urls import path
from .views import generic 
from .views.users import SignUp, SignIn, SignOut, ChangePassword
from .views.blogs import BlogsView, BlogView
from .views.comments import CommentsView, CommentView

urlpatterns = [
    path('', generic.index), #http://127.0.0.1:8000/api/
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-password/', ChangePassword.as_view(), name='change-password'),
    path('blogs/', BlogsView.as_view(), name='blogs'),
    path('blogs/<int:pk>/', BlogView.as_view(), name='blog-detail'),
    path('comments/',   CommentsView.as_view(), name='comments'),
    path('blogs/<int:blog_id>/comments/', CommentView.as_view(), name='blog-comments-list'),
    path('blogs/<int:blog_id>/comments/create/',   CommentsView.as_view(), name='comment-create'),
    # todo: for comments, the put or patch route that verifies the user is the author
    path('blogs/<int:blog_id>/comments/<int:pk>/update/', CommentView.as_view(), name='comment-update'),
    #* Note: you can pass the queryset and serializer as an argment in as_view() - see below 
    #* path('blogs/<int:blog_id>/comments/<int:pk>/update/', CommentView.as_view(queryset=Comment.objects.all(), serializer_class=CommentSerializer), name='comment-update'),
    
    # path('blogs/<int:blog_id>/comments/<int:pk>/delete/', CommentView.as_view(), name='comment-delete'),
    # path('blogs/<int:blog_id>/comments/<int:pk>/', CommentView.as_view(), name='comment-update'),
    # path('blogs/<int:blog_id>/comments/<int:pk>/delete/', CommentView.as_view(), name='comment-delete'),
    # path('blogs/<int:blog_id>/comments/<int:pk>/', CommentView.as_view(), name='comment-like'),
    # path('blogs/<int:blog_id>/comments/<int:pk>/', CommentView.as_view(), name='comment-detail'),
]
