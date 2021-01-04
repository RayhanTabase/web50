from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", blank=True, related_name="watchlist")

class Listing(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name="listings")
    item_name = models.CharField(max_length=30)
    item_description = models.CharField(max_length=1000,null=True, blank=True)
    bid_price = models.DecimalField(decimal_places=2,max_digits=12)
    
    image = models.URLField(blank=True, verbose_name="Image URL", null=True)
    category = models.CharField(max_length = 20)
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="wins", blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.item_name}: ${self.bid_price}"


class Comment(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_cmt",null=False)
    cmt_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item_cmt")
    comment = models.CharField(max_length=30)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.cmt_item.item_name}:  {self.comment}"


class Bid(models.Model):
    bidder = models.ForeignKey(User,on_delete=models.CASCADE,related_name="bid_user")
    item = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="bid_item")
    bid = models.DecimalField(decimal_places=2,max_digits=12)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.bidder.username}:  {self.item.item_name}: ${self.bid}"
   
 

