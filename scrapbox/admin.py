from django.contrib import admin

# Register your models here.
from scrapbox.models import UserProfile,Scrap,WishList

admin.site.register(UserProfile)
admin.site.register(Scrap)
admin.site.register(WishList)