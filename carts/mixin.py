from django.contrib.contenttypes.models import ContentType
from .models import Cart, CartItem

class CartMixin:
    def get_cart(self, request):
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.save()
                session_key = request.session.session_key
            cart, _ = Cart.objects.get_or_create(session_key=session_key)
        return cart

    def render_cart(self, request):
        cart = self.get_cart(request)
        cart_items = cart.items.all()
        total = sum(item.content_object.price * item.quantity for item in cart_items)
        context = {
            'cart_items': cart_items,
            'total': total,
        }
        return render_to_string('cart/cart_items.html', context)