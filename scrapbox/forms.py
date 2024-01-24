from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from scrapbox.models import Scrap,Bids,UserProfile,Reviews

class UserForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]
        
        # widgets={
        #     "username":forms.TextInput(attrs={"class":"form-control"}),
        #     "email":forms.TextInput(attrs={"class":"form-control"}),
        #     "password1":forms.TextInput(attrs={"class":"form-control"}),
        #     "password2":forms.PasswordInput(attrs={"class":"form-control"}),
        # }
    def __init__(self, *args: Any, **kwargs):
        super(UserForm,self).__init__(*args, **kwargs)
        
        self.fields["password1"].widget.attrs["class"]="form-control"
        self.fields["email"].widget.attrs["class"]="form-control"
        self.fields["username"].widget.attrs["class"]="form-control"
        self.fields["password2"].widget.attrs.update({"class":"form-control"})

class SignInForm(forms.Form):
    # username=forms.CharField()
    # password=forms.CharField()
    username=forms.CharField(widget=forms.TextInput(attrs={
        "class":"inputbox",
        "type":"text",
        "placeholder":"enter username",
    }),label="username1")
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        "class":"inputbox ",
        "type":"password",
        "placeholder":"enter password",                             
    }),label="password")

class ScrapCreateForm(forms.ModelForm):
    class Meta:
        model=Scrap
        exclude="user","status"
# class IndexForm(forms.ModelForm):
#     class Meta:
#         model=
#         fields="__all__"
        
    
class BidCreateForm(forms.ModelForm):
    class Meta:
        model=Bids
        fields=["amount"]
     
# class ProfileListForm(forms.ModelForm):
#     class Meta:
#         model=Bids
#         fields=["amount"]

    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude=("user","following","block")
        
        widgets={
            "dob":forms.DateInput(attrs={"class":"form-control","type":"date"})
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model=Reviews
        fields=["comment","rating"]
        
