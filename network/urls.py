
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #API Routes
    path("profile/<int:user_id>",views.profile, name="profile"),
    path("posts",views.allposts,name="allposts"),
    path("is_follower/<int:is_user1>/<int:following_user2>",views.is_follower,name="isFollower"),
    path('follow/<int:user_id>',views.follow,name="follow"),
    path('unfollow/<int:user_id>',views.unfollow,name="unfollow"),
    path('following_posts',views.following_posts,name="following_posts"),
    path('like/<int:post_id>',views.like,name="like")
    
]
