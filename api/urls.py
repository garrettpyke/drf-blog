from django.urls import path
from .views import generic 
from .views.users import SignUp, SignIn, SignOut, ChangePassword
from .views.blogs import BlogsView

urlpatterns = [
    path('', generic.index),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-password/', ChangePassword.as_view(), name='change-password'),
    path('blogs/', BlogsView.as_view(), name='blogs'),
    # path('blogs/<int:pk>/', Blog.as_view(), name='blog-detail'),
    # path('blogs/<int:pk>/comments/', generic.CommentList.as_view(), name='comment-list'),
    # path('blogs/<int:pk>/comments/<int:comment_id>/', generic.CommentDetail.as_view(), name='comment-detail'),
]
