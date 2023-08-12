from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.category}"


class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=120)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=11, decimal_places=2)
    current_bid = models.ForeignKey('Bid', related_name="bid_listings", on_delete=models.CASCADE, blank=True, null=True)
    img_url = models.CharField(max_length=500)
    category = models.ForeignKey(Category, related_name="listings", default="other", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}: ${self.starting_price} by {self.owner.username}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid_amount = models.DecimalField(max_digits=11, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"${self.bid_amount} for {self.listing.title} by {self.user.username}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.listing.title}"


class Watchlist(models.Model):
    user = models.ManyToManyField(User, related_name="watchlist")
    listing = models.ManyToManyField(Listing, related_name="watchlist")

    def __str__(self):
        return f"watchlist"