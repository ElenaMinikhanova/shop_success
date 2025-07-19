from django.contrib import admin
from .models import Catalog
# Register your models here.


@admin.register(Catalog)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['category', 'name']

