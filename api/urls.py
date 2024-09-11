from django.urls import path
from .views import generic 
from .views.users import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
    path('', generic.index),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-password/', ChangePassword.as_view(), name='change-password'),
]
