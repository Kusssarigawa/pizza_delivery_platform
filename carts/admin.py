# admin.py
from django.contrib import admin # type: ignore
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_key', 'created_at', 'total_items')
    inlines = [CartItemInline]

    def total_items(self, obj):
        return obj.items.count()

    total_items.short_description = 'Количество товаров'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'content_object', 'quantity', 'price')
    list_filter = ('cart', 'content_type')
    search_fields = ('cart__id', 'content_object__name')

    def total_price(self, obj):
        return obj.total_price

    total_price.short_description = 'Общая стоимость'
