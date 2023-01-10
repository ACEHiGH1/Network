from django.contrib import admin
from .models import User, Post, Profile

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Profile)
# Register your models here.
