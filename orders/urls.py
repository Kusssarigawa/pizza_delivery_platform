from django.urls import path
from .views import CheckoutView
from carts.urls import *
app_name="order"
urlpatterns = [
   
    path('', CheckoutView.as_view(), name='checkout'),
   

]