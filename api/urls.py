from django.urls import path
from .views import generic 
from .views.users import SignUp

urlpatterns = [
    path('', generic.index),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
]
