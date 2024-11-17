from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from django.contrib.contenttypes.models import ContentType
from menu.models import Pizza, Burger, Drink
import json

class CartBaseView(View):
    def get_cart(self, request):
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
        return cart


class CartView(CartBaseView):
    def get(self, request):
        cart = self.get_cart(request)
        cart_items = cart.items.all().select_related('content_type')
        cart_total = sum(item.quantity * item.price for item in cart_items)
    
        items_data=[{
            'id':item.id,
            'quantity':item.quantity,
            'price':item.price,
            'size':item.size,
            'product_name':item.content_object.name,
            'image': item.content_object.image.url,  # убедитесь, что это правильный путь
        }for item in cart_items]
        return JsonResponse({
            'cart_items': items_data,
            'cart_item_count': cart.items.count(),
            'cart_total':cart_total
        })

class AddToCartView(CartBaseView):
    def post(self, request, product_id, product_type):
        cart = self.get_cart(request)
        data = json.loads(request.body)

        quantity = int(data.get('quantity', 1))
        size = data.get('size')
        price = float(data.get('price'))  # Здесь мы получаем переданную цену с клиента

        # Получаем продукт по его типу
        if product_type == 'pizza':
            product = get_object_or_404(Pizza, id=product_id)
        elif product_type == 'burger':
            product = get_object_or_404(Burger, id=product_id)
        elif product_type == 'drink':
            product = get_object_or_404(Drink, id=product_id)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid product type'})

        # Создаем или обновляем элемент корзины с правильной ценой
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            content_type=ContentType.objects.get_for_model(product),
            object_id=product_id,
            size=size,
            defaults={'quantity': quantity, 'price': price}  # Здесь мы используем динамическую цену
        )

        # Если элемент уже существует, обновляем количество
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity  # Устанавливаем начальное количество

        # Обновляем цену на ту, которая передана с клиента
        cart_item.price = price
        cart_item.save()

        return JsonResponse({
            'success': True,
            'cart_item_count': cart.items.count(),
        })


class RemoveFromCartView(CartBaseView):
    def post(self, request, item_id):
        cart = self.get_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()
        cart_total = sum((item.quantity or 0) * (item.price or 0) for item in cart)
        return JsonResponse({
            'success': True,
            'cart_item_count': cart.items.count(),
            'cart_total': cart_total,
        })

class UpdateCartItemView(CartBaseView):
    def post(self, request, product_id, action):
        cart = self.get_cart(request)
        data = json.loads(request.body)

        cart_item = get_object_or_404(CartItem, cart=cart, id=product_id)

        if action == 'change-size':
            new_size = data.get('size')
            new_price = float(data.get('price', 0))
            if new_size and new_price:
                cart_item.size = new_size
                cart_item.price = new_price
        elif action == 'increment':
            cart_item.quantity += 1
        elif action == 'decrement' and cart_item.quantity > 1:
            cart_item.quantity -= 1

        cart_item.save()

        cart_total = sum(item.quantity * item.price for item in cart.items.all())

        return JsonResponse({
            'success': True,
            'cart_item_count': cart.items.count(),
            'cart_total': cart_total,
            'item_price': cart_item.price,
            'item_quantity': cart_item.quantity,
            'item_total': cart_item.quantity * cart_item.price,
        })