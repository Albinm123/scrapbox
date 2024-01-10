from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
   
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    address=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    dob=models.DateField(null=True)
    bio=models.CharField(max_length=200)
    profile_pic=models.ImageField(null=True,upload_to="images\profile_img")
    
    def __str__(self):
        return self.user.username
       
class Category(models.Model):
    name=models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Scrap(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_srapbox")
    name=models.CharField(max_length=200)
    price=models.IntegerField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="category_scrapbox",null=True)
    condition=models.CharField(max_length=200)
    location=models.CharField(max_length=200)
    created_date=models.DateTimeField(auto_now_add=True,null=True)
    options=(
        ("available","available"),
        ("sold","sold"),
    )
    status=models.CharField(max_length=200,choices=options,default="available")
    scrap_pic=models.ImageField(upload_to="images\scrap_img",null=True)

    def __str__(self):
        return self.name

class Bids(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_bid")
    scrap=models.ForeignKey(Scrap,on_delete=models.CASCADE,related_name="scrap_bid")
    amount=models.IntegerField()
    options=(
        ("pending","pending"),
        ("accept","accept"),
        ("reject","reject"),
    )
    status=models.CharField(max_length=200,choices=options,default="pending")
    
class WishList(models.Model):
    scrap=models.ManyToManyField(Scrap,related_name="scrap_whish")
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_whish")
    created_date=models.DateTimeField(auto_now_add=True)

class Reviews(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_review")
    scrap=models.ForeignKey(Scrap,on_delete=models.CASCADE,related_name="scrap_review")
    comment=models.CharField(max_length=200)
    options=(
        ("1","1"),
        ("2","2"),
        ("3","3"),
        ("4","4"),
        ("5","5"),
    )
    rating=models.CharField(max_length=200,choices=options,default="5")
    
   
def create_profile(sender,created,instance,**kwargs):
     if created:
        UserProfile.objects.create(user=instance)
        print("profile obj creadted")
post_save.connect(create_profile,sender=User)