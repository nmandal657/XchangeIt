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
    path('propose_swap/<int:item_id>/', views.propose_swap, name='propose_swap'),
    path('my_trades/', views.my_trades, name='my_trades'),
    path('respond_swap/<int:proposal_id>/<str:action>/', views.respond_swap, name='respond_swap'),
    path('complete_swap/<int:proposal_id>/', views.complete_swap, name='complete_swap'),
]