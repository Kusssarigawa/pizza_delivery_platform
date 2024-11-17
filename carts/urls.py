# urls.py
from django.urls import path
from .views import CartView, AddToCartView, RemoveFromCartView, UpdateCartItemView
app_name='cart'
urlpatterns = [
    
    path('', CartView.as_view(), name='cart'),
    path('add/<int:product_id>/<str:product_type>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('update/<int:product_id>/<str:action>/', UpdateCartItemView.as_view(), name='update-cart-item'),
]