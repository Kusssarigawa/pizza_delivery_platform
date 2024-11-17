from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),  # Главная страница
    path('about-us/', views.AboutView.as_view(), name='about-us'),  # Страница "О нас"
    path('contacts/', views.ContactsView.as_view(), name='contacts'),  # Контакты
]
