from django.contrib import admin
from .models import Product,Subscriber,Maker
# Register your models here.
admin.site.register(Product)
admin.site.register(Subscriber)
admin.site.register(Maker)
