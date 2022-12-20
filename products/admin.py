from django.contrib import admin

from .models import ProductCategory, Product, Basket


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'short_description', 'price', 'quantity',
                    'category']
    list_per_page = 6
    fields = ['name', 'image', 'description', 'short_description', ('price', 'quantity'), 'category']
    search_fields = ['name']


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_per_page = 5
    ordering = ['name']

class BasketAdminInLine(admin.TabularInline):
    model = Basket
    fields = ['product', 'quantity']
    readonly_fields = ['product']
    extra = 0