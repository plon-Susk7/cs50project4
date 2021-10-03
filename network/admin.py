from django.contrib import admin
from .models import Post,Likes, User,Profile

# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Likes)
admin.site.register(Profile)
