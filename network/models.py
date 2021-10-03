from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case


class User(AbstractUser):
    def serialize(self):
        return{
            "id": self.id,
            "username" : self.username
        }
    
    def __str__(self):
        return f"{self.username}"

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.timestamp}"
    
    def serialize(self):
        return{
            "id":self.id,
            "user_id":self.user.id,
            "user":self.user.username,
            "content" : self.content,
            "timestamp":self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

class Likes(models.Model):
    post = models.OneToOneField(Post,on_delete=CASCADE,related_name="liked_post")
    user = models.ManyToManyField(User,blank=True,null=True,related_name="liker")

    def serialize(self):
        return{
            "post" : self.post.id,
            "likes" : int(self.user.all().count())
        }

    def __str__(self):
        return f"{self.post}"

class Profile(models.Model):
    followers = models.ManyToManyField(User,blank=True,null=True,related_name="followers")
    following = models.ManyToManyField(User,blank=True,null=True,related_name="following")
    user = models.OneToOneField(User,on_delete=CASCADE)
    
    def __str__(self):
        return f"{self.user} {self.followers.all().count()} {self.following.all().count()}"

    def serialize(self):
        return{
            "cuser_id" : self.user.id,
            "followers" : int(self.followers.all().count()),
            "following" : int(self.following.all().count())
        }