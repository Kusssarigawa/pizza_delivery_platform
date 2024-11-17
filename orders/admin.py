from django.contrib import admin
from .models import OrderItem,DeliveryLocation


@admin.register(DeliveryLocation)
class DeliveryLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'working_hours', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'address')
# Register your models here. 
admin.site.register(OrderItem)