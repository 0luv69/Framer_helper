from django.contrib import admin
from .models import *


# User admin 
admin.site.register(FramerInfo)
admin.site.register(BuyersInfo)


# Product amdin page view
class ProductImg_Admin(admin.StackedInline):
    model = ProductImages

@admin.register(Product)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display= ['title','price','discription']

    inlines= [ProductImg_Admin]

admin.site.register(ProductImages)



