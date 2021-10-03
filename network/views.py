
from django.contrib.auth import authenticate, login, logout
from django.core import paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Post,Likes
from .forms import addPost
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core import serializers
from .models import *
import json
from django.core.paginator import Paginator

from .models import User


def index(request):
    form  = addPost(request.POST)
    if request.method == "POST":
     if form.is_valid():
         newPost = form.save(commit=False)
         newPost.user = request.user
         newPost.save()
         like = Likes.objects.create(post=newPost)
         like.save()

    return render(request, "network/index.html",{
        "form": addPost()
    })

@login_required
def allposts(request):
         
         posts  = Post.objects.order_by("-timestamp").all()
         return JsonResponse([post.serialize() for post in posts], safe=False)



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))





def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

            profile = Profile.objects.create(user=user)
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profile(request,user_id):
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter( user = user).order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)

def is_follower(request, is_user1, following_user2):
    try:
        is_user1 = User.objects.get(id = is_user1)
        following_user2 = User.objects.get(id = following_user2)

        followers_user2 = Profile.objects.get(user = following_user2).followers.all()

        if followers_user2.filter(username = is_user1).count() > 0:
            result = True
        else:
            result = False

        return JsonResponse({
                "result": result
            }, status=200)
    except:
        return JsonResponse({
                "result": False
            }, status=400)

def follow(request,user_id):
    user_profile = Profile.objects.get(user=user_id)
    if request.method == "GET":
        return JsonResponse(user_profile.serialize(),safe=False)

    if request.method=="PUT":
        cuser_id= request.user.id

        data = json.loads(request.body)

        if data.get("cuser_id") is not None:
            followed_user_id = data["cuser_id"]
        
        current_user = User.objects.get(pk=cuser_id)
        followed_user = User.objects.get(pk=followed_user_id)

        get_profile = Profile.objects.get(user = current_user)
        get_profile.following.add(followed_user)

        get_followed_profile = Profile.objects.get(user=followed_user)
        get_followed_profile.followers.add(current_user)

        get_profile.save()
        get_followed_profile.save()

        return HttpResponse(status=204)

   
def unfollow(request,user_id):
    user_profile = Profile.objects.get(user=user_id)
    if request.method == "GET":
        return JsonResponse(user_profile.serialize(),safe=False)
    

    if request.method=="PUT":
        cuser_id= request.user.id

        data = json.loads(request.body)

        if data.get("cuser_id") is not None:
            followed_user_id = data["cuser_id"]
        
        current_user = User.objects.get(pk=cuser_id)
        unfollowed_user = User.objects.get(pk=followed_user_id)

        get_profile = Profile.objects.get(user = current_user)
        get_profile.following.remove(unfollowed_user)

        get_unfollowed_profile = Profile.objects.get(user=unfollowed_user)
        get_unfollowed_profile.followers.remove(current_user)

        get_profile.save()
        get_unfollowed_profile.save()

        return HttpResponse(status=204)

def following_posts(request):
    get_currentUser = User.objects.get(pk=request.user.id)
    current_user = Profile.objects.get(user =get_currentUser)

    following_users = current_user.following.all()
    posts = []
    for following_user in following_users:
         posts += Post.objects.filter( user = following_user).order_by("-timestamp").all()
         
    return JsonResponse([post.serialize() for post in posts], safe=False)

@csrf_exempt    
def like(request,post_id):
    cuser= request.user
    post = Post.objects.get(pk=post_id)
    post1 = Likes.objects.get(post=post_id)

    if request.method == "GET":
        return JsonResponse(post1.serialize())
    
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get('like'):
            post_like = Likes.objects.get(post = post)
            post_like.user.add(cuser)     
        else:
            post_like = Likes.objects.get(post = post)
            post_like.user.remove(cuser)
        
        post_like.save()
        return HttpResponse(status=204)
            