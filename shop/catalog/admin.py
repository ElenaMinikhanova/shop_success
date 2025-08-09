from django.contrib import admin
from .models import Product, PhotoProduct, Category, Stocks, UserInfo, OrderHistory, Order
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

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['stock'].required = False
        return form

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name',)

@admin.register(UserInfo)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('user',)

class OrderInline(admin.TabularInline):
    model = Order
    extra = 0  # Не добавлять лишних пустых строк

@admin.register(OrderHistory)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderInline]
    list_display = ('id', 'user', 'status', 'date_order', 'date_status')
    list_editable = ('status',)


admin.site.register(Order)