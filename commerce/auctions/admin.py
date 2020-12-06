from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)
admin.site.register(Create_Listing)
admin.site.register(Bid)
admin.site.register(Comments)
admin.site.register(Watchlist)
admin.site.register(Category)