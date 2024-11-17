from django.db import models
from django.utils import timezone
from menu.models import Pizza, Burger, Drink  # Импортируем модели продуктов
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

class Cart(models.Model):
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id}"


    def get_total_cost(self):
        return sum(item.get_total_cost() for item in self.items.all())
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Фиксированная цена товара на момент добавления

    def __str__(self):
        return f"{self.content_object} ({self.quantity})"

    
    def get_total_price(self):
        """Подсчитывает общую стоимость позиции в корзине."""
        return self.quantity * self.price

    def get_total_cost(self):
        return self.quantity  * self.content_object.price
    
    