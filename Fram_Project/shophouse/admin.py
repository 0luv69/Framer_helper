from django.contrib import admin
from .models import *


# Product amdin page view
class ProductImg_Admin(admin.StackedInline):
    model = ProductImages

@admin.register(Product)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display= ['title','price','discription']

    inlines= [ProductImg_Admin]

admin.site.register(ProductImages)

admin.site.register(Categories)
admin.site.register(Cart)
admin.site.register(CheckOutInfo)
admin.site.register(ShippingInfo)