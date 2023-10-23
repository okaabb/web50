from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.decorators import login_required


class User(AbstractUser):
    pass


class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=0)
    user_username = models.TextField(default="None")
    listing_id = models.IntegerField(default=0)
    bid = models.IntegerField(default=0)


class Category(models.Model):
    name = models.CharField(primary_key=True, max_length=64)

    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    description = models.TextField()
    current_bid = models.IntegerField()
    available = models.BooleanField()
    pic_url = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user_id = models.IntegerField(default=0)
    user_username = models.TextField(default="None")
    bids = models.IntegerField(default=0)
    bid_winner = models.TextField(default="None")
    min_bid = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.id}"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    body = models.TextField(blank=True, default="None")
    user_id = models.IntegerField(default=0)
    user_username = models.TextField(default="None")
    listing_id = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user_id} ({self.id}):"


class closeBid(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=0)
    user_username = models.TextField(default="None")
    listing_id = models.IntegerField(default=0)


class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=0)
    user_username = models.TextField(default="None")
    listing_id = models.IntegerField(default=0)
    title = models.TextField()
    pic_url = models.TextField(blank=True)
