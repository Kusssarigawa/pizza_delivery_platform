from django.contrib import admin
from .models import  Pizza, Burger, Drink, Ingredient

# Админка для категории
# @admin.register(Categories)
# class CategoriesAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ("name",)}
#     list_display = ["name", "slug"]
#     search_fields = ["name"]
#     list_filter = ["name"]
#     fields = ["name", "slug"]

# Админка для пиццы
@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "size", "price", "image"]  # Добавляем поле 'image'
    list_editable = ["price"]
    search_fields = ["name", "description"]
    list_filter = ["size", "price"]
    fields = [
        "name",
        "description",
        "size",
        "slug",
        "ingredients",
        "image",  # Добавляем поле 'image'
        ("price",)
    ]

# Админка для бургеров
@admin.register(Burger)
class BurgerAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "price", "image"]  # Добавляем поле 'image'
    list_editable = ["price"]
    search_fields = ["name", "description"]
    list_filter = ["price"]
    fields = [
        "name",
        "description",
        "slug",
        "ingredients",
        "image",  # Добавляем поле 'image'
        ("price",)
    ]

# Админка для напитков
@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "size", "price", "image"]  # Добавляем поле 'image'
    list_editable = ["price"]
    search_fields = ["name"]
    list_filter = ["price", "size"]
    fields = [
        "name",
        "size",
        "slug",
        "image",  # Добавляем поле 'image'
        ("price",)
    ]

# Админка для ингредиентов
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ["name", "extra_price"]
    list_editable = ["extra_price"]
    search_fields = ["name"]
    list_filter = ["name"]
    fields = ["name", "extra_price"]
