"""
URL configuration for scrapboxapplication project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from scrapbox import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.SignInView.as_view(),name="signin"),
    path('register',views.RegistrationView.as_view(),name="register"),
    path('index',views.IndexView.as_view(),name="index"),
    path('create',views.ScrapCreateView.as_view(),name="scrap_create"),
    path('index/<int:pk>',views.ScrapListView.as_view(),name="scrap_details"),
    path('bids/<int:pk>',views.ScrapBidView.as_view(),name="scrap_bid"),
    path('signout',views.SignoutView.as_view(),name="signout"),
    path('profile/<int:pk>/change',views.ProfileUpdateView.as_view(),name="profile-update"),
    path('profile/<int:pk>',views.ProfileListView.as_view(),name="profile_details"),
    path('scrap/<int:pk>/acept',views.BidAceptView.as_view(),name="bid"),
    path('scrap/<int:pk>/whishlist',views.WhishLlstView.as_view(),name="whishlist"),
    path('scrap/<int:pk>/whishlist/list',views.WishlistDisplayView.as_view(),name="whishlist_list"),
    path('scrap/<int:pk>/review/add',views.ReviewCreateView.as_view(),name="add_review"),
    path('user_bids/', views.UserBidsView.as_view(), name='user_bids'),
    # path('scrap/<int:pk>/add-review/',views.ReviewCreateView.as_view(), name='add_review'),



    # path('bids/<int:pk>',views.bidconView.as_view(),name="bidcon")
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
