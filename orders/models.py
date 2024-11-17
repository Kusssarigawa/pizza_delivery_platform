from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator
from decimal import Decimal
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from menu.models import *
from carts.models import *

class Order(models.Model):
    DELIVERY_CHOICES = [
        ('pickup', 'Самовывоз'),
        ('delivery', 'Доставка'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтвержден'),
        ('preparing', 'Готовится'),
        ('delivering', 'В пути'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменен'),
    ]

    # Основная информация о заказе
    session_key = models.CharField(max_length=40, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Пользователь")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    comment =models.CharField(max_length=100,default='',verbose_name="Коментарии" )
    # delivery_address =models.CharField(max_length=100,default='',verbose_name="Аддрес доставки" )
    # Контактная информация
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате: '+999999999'"
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")

    # Информация о доставке - обновленная часть
    delivery_type = models.CharField(
        max_length=20, 
        choices=DELIVERY_CHOICES, 
        default='pickup',  # Устанавливаем значение по умолчанию
        verbose_name="Способ получения"
    )
    address = models.TextField(
        null=True, 
        blank=True, 
        verbose_name="Адрес доставки",
        help_text="Заполните при выборе доставки"
    )
    pickup_location = models.ForeignKey(
        'DeliveryLocation',
        on_delete=models.SET_NULL,
        null=True, 
        blank=True, 
        verbose_name="Точка самовывоза",
        help_text="Выберите при самовывозе"
    )

    # Финансовая информация
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Сумма заказа")
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Стоимость доставки")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    # def __str__(self):
    #     return f"Заказ {self.order_number}"

    # def save(self, *args, **kwargs):
    #     if not self.order_number:
    #         # Генерация номера заказа
    #         last_order = Order.objects.order_by('-id').first()
    #         if last_order:
    #             last_number = int(last_order.order_number[3:])
    #             self.order_number = f"ORD{str(last_number + 1).zfill(6)}"
    #         else:
    #             self.order_number = "ORD000001"
    #     super().save(*args, **kwargs)

    def get_total_cost(self):
        return self.total_amount + self.delivery_cost

    def clean(self):
        from django.core.exceptions import ValidationError
        
        if self.delivery_type == 'delivery' and not self.address:
            raise ValidationError('При выборе доставки необходимо указать адрес')
        elif self.delivery_type == 'pickup' and not self.pickup_location:
            raise ValidationError('При выборе самовывоза необходимо указать точку получения')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Заказ")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    name = models.CharField(max_length=100)  # Название продукта
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=10, blank=True)
    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"

    def get_total_price(self):
        return self.price * self.quantity
    

class DeliveryLocation(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    working_hours = models.CharField(max_length=100, verbose_name="Часы работы")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Точка выдачи"
        verbose_name_plural = "Точки выдачи"

    def __str__(self):
        return self.name