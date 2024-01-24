from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from scrapbox.models import Scrap,Bids,UserProfile,WishList,Reviews
from scrapbox.forms import UserForm,SignInForm,ScrapCreateForm,BidCreateForm,UserProfileForm,ReviewForm
from django.views.generic import View,CreateView,FormView,DetailView,ListView,UpdateView
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse

# Create your views here.
class RegistrationView(CreateView):
    template_name="register.html"
    form_class=UserForm
    
    def get_success_url(self):
        return reverse("signin")
    
    
    # def get(self,request,*args,**kwargs):
    #     form=UserForm()
    #     return render(request,"register.html",{"form":form})
            
    # def post(self,request,*args,**kwargs):
    #     form=UserForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         print("valid")
    #         return redirect("signin")
    #     else:
    #         print("invalid")
    #         return render(request,"register.html",{"form":form})
               
class SignInView(FormView):
    template_name="signin.html"
    form_class=SignInForm
    
    def post(self,request,*args,**kwargs):
        form=SignInForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwds=form.cleaned_data.get("password")
            user_obj=authenticate(username=uname,password=pwds)
            if user_obj:
                login(request,user_obj)
                print("valid")
                return redirect("index")
        return render(request,"signin.html",{"form":form})
        
class SignoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")

class IndexView(View):
    def get(self,request,*args,**kwargs):
        qs=Scrap.objects.all().exclude(user=request.user)
        wish=WishList.objects.get(user=request.user)
        # print(qs)
        return render(request,"index.html",{"data":qs,"wish":wish})
    
    # def post(self,request,*args,**kwargs):
    #     return render(request,"index.html")
    
class ScrapCreateView(CreateView):
    template_name="scrapcreate.html"
    form_class=ScrapCreateForm
    model=Scrap
    
    def get_success_url(self):
        return reverse("index")
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)

    # def get(self,request,*args,**kwargs):
    #     form=ScrapCreateForm()
    #     return render(request,"scrapcreate.html",{"form":form})
    
    # def post(self,request,*args,**kwargs):
    #     form=ScrapCreateForm(request.POST,files=request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         print("success")
    #         return redirect("index")
    #     else:
    #         # print("faild")
    #         return render(request,"scrapcreate.html",{"form":form})

class ScrapListView(DetailView,CreateView):
    template_name="scrap_details.html"
    model=Scrap
    form_class=ReviewForm
    context_object_name="data"
    
    def get_context_data(self,**kwargs):
        context =super().get_context_data(**kwargs)
        id=self.kwargs.get("pk")
        print(".....",id)
        scrap_obj=Scrap.objects.get(id=id)
        context["reviews"]=Reviews.objects.filter(scrap=scrap_obj)
        context["wish"]=WishList.objects.get(user=self.request.user)

        return context
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     id = self.kwargs.get("pk")
    #     scrap_obj = Scrap.objects.get(id=id)
    #     context["reviews"] = Reviews.objects.filter(scrap=scrap_obj)
    #     context["form"] = ReviewForm()
    #     return context

class ScrapDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        qs=Scrap.objects.get(id=id).delete()
        return redirect("login")

class ScrapBidView(View):
    # template_name="bids.html"
    # form_class=BidCreateForm
    # model=Bids
    
    # def form_valid(self,form):
    #     form.instance.user=self.request.user
    #     form.instance.scrap=self.request.scrap
    #     return super().form_valid(form)


    def get(self,request,*args,**kwargs):
        form=BidCreateForm()
        id=kwargs.get("pk")
        qs=Scrap.objects.get(id=id)
        return render(request,"bids.html",{"form":form,"data":qs})
    
    def post(self,request,*args,**kwargs):
        form=BidCreateForm(request.POST)
        id=kwargs.get("pk")
        scrap=Scrap.objects.get(id=id)
        # print(scrap_id)
        if form.is_valid:
            form.instance.scrap=scrap
            form.instance.user=request.user
            form.save()
            return redirect("index")

class ProfileListView(DetailView):
    template_name="profile.html"
    model=UserProfile
    context_object_name="data"   
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the Scrap model to the context
        context['scrap_object'] = Scrap.objects.all().filter(user = self.request.user )
        # context['bid_objects'] = Bids.objects.filter(user=self.request.user)
        context['bid_objects'] = Bids.objects.all()
        # filter(scrap__user= self.request.user)       
        # # Set a custom context_object_name for the Scrap model
        context['scrap_data'] = context['scrap_object']
        context['bid_data'] = context['bid_objects']

        
        
        return context
    
class ProfileUpdateView(UpdateView):
     template_name="profile_add.html"
     form_class=UserProfileForm
     model=UserProfile
     
     def get_success_url(self):
         return reverse("index")
     
class BidAceptView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        print(id)
        bid_obj=Bids.objects.get(id=id)
        
        action=request.POST.get("action")
        if action=="accept":
            bid_obj.status="accept"
            bid_obj.save()
            other_bids = Bids.objects.filter(scrap=bid_obj.scrap, user=bid_obj.user).exclude(id=id)
            for bid in other_bids:
                bid.status = "reject"
                bid.save()
            print("s")
        # elif action=="decline":
        #     # request.user.profile.block.remove(profile_obj)
        #     bid_obj.status="reject"
        #     bid_obj.save()

        return redirect("index")
    
class WhishLlstView(View):

        def post(self,request,*args,**kwargs):
            id=kwargs.get("pk")
            scrap_obj=Scrap.objects.get(id=id)
            user=request.user
            action=request.POST.get("action")

            # wishlist=WishList.objects.get_or_create(user=user)
            wishlist_exists = WishList.objects.filter(user=user).exists()
            if not wishlist_exists:
                wishlist = WishList.objects.create(user=user)
            else:
                wishlist = WishList.objects.get(user=user)
            
            if action == "remove_whishlist":
                wishlist.scrap.remove(scrap_obj)
            elif action == "add_to_whishlist":
                wishlist.scrap.add(scrap_obj)
            return redirect("index")
        
        # def post(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     scrap_obj=Scrap.objects.get(id=id)
    #     user=request.user
    #     action=request.POST.get("action")

    #     # wishlist, created = WishList.objects.get_or_create(user=user)
    #     # wishlist = WishList.objects.filter(scrap=scrap_obj)
    #     wishlist = WishList.objects.get_or_create(user=user, scrap=scrap_obj)
    #     if wishlist is None:
    #         if action=="remove_whishlist":
    #             wishlist.scrap.remove(scrap_obj)
    #         elif action=="add_to_whishlist":
    #             wishlist.user=(user)
    #             wishlist = WishList.objects.create(user=user)
    #             WishList.objects.add(scrap_obj)
           
            
    #     return redirect("index")
    
    # def post(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     scrap_obj=Scrap.objects.get(id=id)
    #     action=request.POST.get("action")
    #     wishlist = WishList.objects.get_or_create(user=request.user)
    #     if action == "add":
    #         wishlist.scrap.add(scrap_obj)
    #     elif action == "remove":
    #         wishlist.scrap.remove(scrap_obj)
    #     return redirect("index")
    
    
class WishlistDisplayView(View):
    def get(self,request,*args,**kwargs):
        qs=WishList.objects.filter(user=request.user)
        wish=WishList.objects.get(user=request.user)
        return render(request,"whishlist.html",{"data":qs,"wish":wish})
    
    
class ReviewCreateView(CreateView):
    # template_name="scrap_details.html"
    form_class=ReviewForm
    model=Reviews
    
    def get_success_url(self):
        # return reverse("add_review")
        return reverse("scrap_details", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        form.instance.user=self.request.user
        id=self.kwargs.get("pk")
        # print(id)
        scrap_obj=Scrap.objects.get(id=id)
        form.instance.scrap=scrap_obj
        return super().form_valid(form)
    
    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     id=self.kwargs.get("pk")
    #     print(".....",id)
    #     scrap_obj=Scrap.objects.get(id=id)
    #     context["reviews"]=Reviews.objects.all()
    #     return context
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     id = self.kwargs.get("pk")
    #     scrap_obj = Scrap.objects.get(id=id)
    #     # context['scrap'] = scrap_obj
    #     context['reviews'] = Reviews.objects.filter(scrap=scrap_obj)
    #     return context
    
    # def get_queryset(self):
    #     id=self.kwargs.get("pk")
    #     qs=Scrap.objects.get(id=id)
    #     return qs

    # def get(self,request,*args,**kwargs):
    #     form=ReviewForm()
    #     return render(request,"rev.html",{"form":form})
    
    # def post(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     scrap_obj=Scrap.objects.get(id=id)
    #     user=request.user
    #     scrap=scrap_obj

# class ReviewCreateView(CreateView):
    #     model = Reviews
    #     form_class = ReviewForm

    #     def form_valid(self, form):
    #         form.instance.user = self.request.user
    #         id = self.kwargs.get("pk")
    #         scrap_obj = Scrap.objects.get(id=id)
    #         form.instance.scrap = scrap_obj
    #         return super().form_valid(form)

    #     def get_success_url(self):
    #         id = self.kwargs.get("pk")
    #         return reverse("scrap_details", kwargs={"pk": id})
    
class UserBidsView(View):
    template_name = 'user_bids.html'

    def get(self, request, *args, **kwargs):
        # Retrieve the user's bids
        user_bids = Bids.objects.filter(user=request.user)
        
        context = {
            'user_bids': user_bids,
        }

        return render(request, self.template_name, context)