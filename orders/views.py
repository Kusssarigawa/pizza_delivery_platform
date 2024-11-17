from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from .models import Order, OrderItem
from .forms import CheckoutForm
from carts.models import Cart, CartItem

class CheckoutView(View):
    def get(self, request):
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        # Получаем корзину по session_key
        cart = get_object_or_404(Cart, session_key=session_key)
        cart_items = CartItem.objects.filter(cart=cart)
        cart_total = sum(item.quantity * item.price for item in cart_items)
        # Инициализация формы
        form = CheckoutForm()

        return render(request, 'checkout.html', {
            'cart_items': cart_items,
            'cart_total': cart_total,
            'form': form
        })

    def post(self, request):
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        cart = get_object_or_404(Cart, session_key=session_key)
        cart_items = CartItem.objects.filter(cart=cart)

        # Получаем данные из формы
        form = CheckoutForm(request.POST)
        if form.is_valid():
            delivery_type = form.cleaned_data['delivery_type']

            # Проверяем, указан ли пункт самовывоза, если выбран способ самовывоза
            if delivery_type == 'pickup' and not form.cleaned_data.get('pickup_location'):
                form.add_error('pickup_location', 'Пожалуйста, выберите точку получения.')
                return JsonResponse({'success': False, 'errors': {'pickup_location': ['Пожалуйста, выберите точку получения.']}})

            # Если форма валидна, создаем заказ
            order = Order.objects.create(
                session_key=session_key,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                delivery_type=delivery_type,
                pickup_location=form.cleaned_data['pickup_location'] if delivery_type == 'pickup' else None,
                address=form.cleaned_data['address'] if delivery_type == 'delivery' else None,
                total_amount=cart.get_total_cost(),
                comment=form.cleaned_data['comment'],
            )
            # Добавляем позиции корзины как элементы заказа
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    content_type=item.content_type,
                    quantity=item.quantity,
                    price=item.price,
                    total_price=item.get_total_cost(),
                    object_id=item.object_id,
                    size=item.size
                )

            # Очищаем корзину после оформления заказа
            cart_items.delete()

            # Возвращаем успешный JSON ответ
            return JsonResponse({'success': True, 'message': 'Ваш заказ успешно оформлен!'})
        else:
            # Если форма не валидна, возвращаем ошибки
            errors = {field: list(form.errors[field]) for field in form.errors}
            return JsonResponse({'success': False, 'errors': errors})
