from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.home),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('add_item/', views.add_item, name='add_item'),
    path('view_profile/<int:user_id>/', views.view_profile, name='view_profile'),
]