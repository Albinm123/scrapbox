from django.test import TestCase

# Create your tests here.

    # def post(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     scrap_obj=Scrap.objects.get(id=id)
    #     user=request.user
    #     action=request.POST.get("action")

    #     # wishlist, created = WishList.objects.get_or_create(user=user)
    #     # wishlist = WishList.objects.filter(scrap=scrap_obj)
    #     wishlist = WishList.objects.filter(user=user, scrap=scrap_obj)
    #     if wishlist is None:
    #         if action=="remove_whishlist":
    #             # wishlist.user=(user)
    #             wishlist.scrap.remove(scrap_obj)
    #             # wishlist = WishList.objects.create(user=user)
    #             # wishlist.scrap.add(scrap_obj)
    #         elif action=="add_to_whishlist":
    #             wishlist = WishList.objects.create(user=user)
    #             WishList.objects.add(scrap_obj)
    #             # wishlist.scrap.add(scrap_obj)
    #             # wishlist.scrap.remove(scrap_obj)
            
    #     return redirect("index")