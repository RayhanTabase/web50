from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("User",related_name="user_followers",blank=True)
    following = models.ManyToManyField("User",related_name="user_followings",blank=True)
    
    def serialize(self):
        return {
                "id": self.id,
                "username": self.username,
                "followers":[user.username for user in self.followers.all()],
                "following": [user.username for user in self.following.all()],
            }

class Post(models.Model):
    creator = models.ForeignKey("User", on_delete=models.CASCADE,related_name="post")
    post = models.CharField(max_length=1000)
    likes = models.ManyToManyField("User",related_name="post_likes",blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "creator": self.creator.username,
            "creator_id":self.creator.id,
            "likes": [user.username for user in self.likes.all()],
            "post": self.post,           
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }

class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE,related_name="post_comments")
    creator = models.ForeignKey("User", on_delete=models.PROTECT,related_name="user_comments")
    comment = models.CharField(max_length=1000)
    likes = models.ManyToManyField("User",related_name="comment_likes",blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    def serialize(self):
        return {
            "id": self.id,
            "creator": self.creator.username,
            "comment": self.comment, 
            "likes": [user.username for user in self.likes.all()],          
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }
