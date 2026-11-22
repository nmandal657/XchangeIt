from django.contrib import admin

# Register your models here.
from .models import User, UserProfile, Item, TradeProposal

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Item)
admin.site.register(TradeProposal)