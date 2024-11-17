# from typing import Any
# from django.db.models.base import Model as Model
# from django.db.models.query import QuerySet
# from django.shortcuts import render
from .models import Pizza, Burger, Drink
from django.views.generic import TemplateView,DetailView



class MenuListView(TemplateView):
    template_name = 'menu.html'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pizzas'] = Pizza.objects.all()  # Пиццы
        context['burgers'] = Burger.objects.all()  # Бургеры
        context['drinks'] = Drink.objects.all()  # Напитки
        context['title'] = 'Меню'  # Заголовок страницы

        return context
 
# def menu(request):
#     pizzas = Pizza.objects.all()
#     burgers = Burger.objects.all()
#     drinks = Drink.objects.all()
    
#     context = {
#         'pizzas': pizzas,
#         'burgers': burgers,
#         'drinks': drinks,
#     }
#     return render(request, 'menu.html', context)

class ProductDetailView(DetailView):
    template_name = 'product_detail.html'
    
    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        # Попробуем найти продукт по слагу в разных моделях
        try:
            return Pizza.objects.get(slug=slug)
        except Pizza.DoesNotExist:
            pass
        
        try:
            return Burger.objects.get(slug=slug)
        except Burger.DoesNotExist:
            pass
        
        try:
            return Drink.objects.get(slug=slug)
        except Drink.DoesNotExist:
            pass
        
        # Если ничего не найдено
        raise Http404("Продукт не найден")
