from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", related_name="user")

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=40)
    image = models.URLField(blank=True)
    status = models.BooleanField(default=True)
    category = models.CharField(max_length=16)
    datetime = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    startingbid = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"${self.bid} bid on {self.listing}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} | {self.listing}"
