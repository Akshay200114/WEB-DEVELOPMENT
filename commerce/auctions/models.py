from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Create_Listing(models.Model):
    Title= models.CharField(max_length=100)
    bid=models.PositiveIntegerField()
    Image=models.URLField()
    Description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True, null=True)
    created_by=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    active=models.BooleanField(default=True)

    
    def __str__(self):
        return f"{self.Title} {self.created_at} {self.created_by}"

class Bid(models.Model):
    user_bid=models.ForeignKey(User,on_delete=models.CASCADE, related_name="Created_user")
    listing_bid=models.ForeignKey(Create_Listing,on_delete=models.CASCADE,related_name="bid_item")
    bid_value=models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user_bid}+{self.listing_bid}"
    
    class Meta:
        ordering=["bid_value"]

class Comments(models.Model):
    user_comment=models.ForeignKey(User, on_delete=models.CASCADE)
    item_comment=models.ForeignKey(Create_Listing, on_delete=models.CASCADE)
    comment=models.CharField(max_length=64)

    def __str__(self):
        return f"{self.user_comment}"

class Watchlist(models.Model):
    user_watchlist=models.ForeignKey(User, on_delete=models.CASCADE)
    watchlist=models.ForeignKey(Create_Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.watchlist}"


class Category(models.Model):
    cat_user=models.ForeignKey(User, on_delete=models.CASCADE)
    cat_item=models.ForeignKey(Create_Listing, on_delete=models.CASCADE)
    category=models.CharField(max_length=64)

    def __str__(self):
        return self.category

    class Meta:
        ordering=['category']


