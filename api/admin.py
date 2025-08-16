from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models.user import MyUser
from .models.blog import Blog

# Register your models here.
admin.site.register(MyUser)
admin.site.register(Blog)