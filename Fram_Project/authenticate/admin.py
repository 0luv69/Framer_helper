from django.contrib import admin
from authenticate.models import *

# Register your models here.
admin.site.register(Profile)

admin.site.register(FramerUser)
admin.site.register(BuyerUser)
