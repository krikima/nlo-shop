from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'in_stock']
    list_editable = ['price', 'stock', 'in_stock']
    list_filter = ['in_stock']
    search_fields = ['name']