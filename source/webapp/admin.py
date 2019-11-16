from django.contrib import admin

# Register your models here.
from webapp.models import Product, Review

admin.site.register(Product)
admin.site.register(Review)