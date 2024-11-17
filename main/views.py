 # Импортируйте модели заказа и позиции заказа
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import login


class IndexView(TemplateView):  
    template_name='index.html'
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["title"] = "PizzaHouse"
        return context

class AboutView(TemplateView):
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["title"] = "Info"
        return context
    template_name='about-us.html'
    

class ContactsView(TemplateView):
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["title"] ="Contact Info" 
        return context
    template_name="contacts.html"
    
# def index(request):
#     return render(request, 'index.html')
# def about_us(request):
#     return render(request, 'about-us.html')
# def contacts(request):
#     return render(request, 'contacts.html')
