from django.contrib import admin
from .models import Film, Basket
# Register your models here.

class InfoAdmin(admin.ModelAdmin):
    fieldsets = [
        ("User Info:", {"fields": ["name","date","done"]}),
        ("Films:", {"fields": ["BasketGenre"]}),
    ]
    
admin.site.register(Basket)
admin.site.register(Film, InfoAdmin)