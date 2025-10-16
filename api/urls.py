from django.urls import path
from .views import generic 
from .views.users import SignUp, SignIn, SignOut, ChangePassword, UsersList
from .views.blogs import BlogsView, BlogsAuthorView, BlogsCategoryView, BlogView
from .views.comments import CommentsView, CommentView
from .views.votes import BlogVotesView

urlpatterns = [
    path('', generic.index), #http://127.0.0.1:8000/api/
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-password/', ChangePassword.as_view(), name='change-password'),
    path('blogs/', BlogsView.as_view(), name='blogs'),
    path('blogs/author/<int:id>/', BlogsAuthorView.as_view(), name='blogs-author'),
    path('blogs/category/<int:pk>/', BlogsCategoryView.as_view(), name='blogs-category'),
    path('blog/<int:pk>/', BlogView.as_view(), name='blog-detail'), # todo: include votes!
    path('comments/',   CommentsView.as_view(), name='comments'),
    path('blog/<int:blog_id>/comments/', CommentView.as_view(), name='blog-comments-list'),
    path('blog/<int:blog_id>/comment/create/',   CommentsView.as_view(), name='comment-create'),
    path('blog/comment/<int:pk>/', CommentView.as_view(), name='comment-detail'),
    path('blog/<int:pk>/vote/', BlogVotesView.as_view(), name="blog-vote"),
    path('users/', UsersList.as_view(), name='users-list'),
    #* Note: you can pass the queryset and serializer as an argment in as_view() as shown below
    #* path('blogs/<int:blog_id>/comments/<int:pk>/update/', CommentView.as_view(queryset=Comment.objects.all(), serializer_class=CommentSerializer), name='comment-update'),
]
