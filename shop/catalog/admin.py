from django.contrib import admin
from .models import Product, PhotoProduct, Category, Stocks, UserInfo
# Register your models here.

class PhotoProductInline(admin.TabularInline):
    model = PhotoProduct
    extra = 1

@admin.register(Stocks)
class StocksAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount')
    list_filter = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('name',)
    inlines = [PhotoProductInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name',)

@admin.register(UserInfo)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('user',)
