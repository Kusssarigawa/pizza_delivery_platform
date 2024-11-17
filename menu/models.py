from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
# class Categories(models.Model):
#     name = models.CharField(max_length=150, unique=True, verbose_name='Название')
#     slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

#     class Meta:
#         db_table = 'category'
#         verbose_name = 'Категорию'
#         verbose_name_plural = 'Категории'
#         ordering = ("id",)

#     def __str__(self):
#         return self.name


class Pizza(models.Model):
    PIZZA_SIZES = [
        ('small', 'Small (25cm)'),
        ('medium', 'Medium (30cm)'),
        ('large', 'Large (40cm)'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    size = models.CharField(max_length=6, choices=PIZZA_SIZES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    ingredients = models.ManyToManyField('Ingredient', blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    image = models.ImageField(upload_to='pizzas/', blank=True, null=True, verbose_name="Изображение")  # Add image field
    
    class Meta:
        db_table = 'Pizza'
        verbose_name = 'Пица'
        verbose_name_plural = 'Пицы'
        ordering = ['price']

    def __str__(self):
        return f"{self.name} ({self.get_size_display()}) - {self.price} грн"


class Burger(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    ingredients = models.ManyToManyField('Ingredient', blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    image = models.ImageField(upload_to='burgers/', blank=True, null=True, verbose_name="Изображение")  # Add image field
    
    class Meta:
        db_table = 'Burgers'
        verbose_name = 'Бургер'
        verbose_name_plural = 'Бургеры'
        ordering = ['price']

    def __str__(self):
        return f"{self.name} - {self.price} грн"


class Drink(models.Model):
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=10)  # Например, '0.5L'
    price = models.DecimalField(max_digits=6, decimal_places=2)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    image = models.ImageField(upload_to='drinks/', blank=True, null=True, verbose_name="Изображение")  # Add image field
    
    class Meta:
        db_table = 'Drinks'
        verbose_name = 'Напиток'
        verbose_name_plural = 'Напитки'
        ordering = ['price']

    def __str__(self):
        return f"{self.name} ({self.size}) - {self.price} грн"


class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    extra_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    class Meta:
        db_table = 'Ingradient'
        verbose_name = 'Инградиент'
        verbose_name_plural = 'Инградиенты'
        ordering = ['name']

    def __str__(self):
        return self.name
