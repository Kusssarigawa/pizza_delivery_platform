 # Импортируйте модели заказа и позиции заказа
from django.shortcuts import render, redirect
from .models import Pizza, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth import login
def menu_view(request):
    pizzas = Pizza.objects.filter(available=True)
    return render(request, 'menu/menu.html', {'pizzas': pizzas})

def create_order_view(request):
    if request.method == 'POST':
        customer = request.user
        order = Order.objects.create(customer=customer)
        
        for pizza_id in request.POST.getlist('pizzas'):
            pizza = Pizza.objects.get(id=pizza_id)
            quantity = int(request.POST.get(f'quantity_{pizza_id}', 1))
            OrderItem.objects.create(order=order, pizza=pizza, quantity=quantity)
        
        return redirect('order_detail', order_id=order.id)
    
    pizzas = Pizza.objects.filter(available=True)
    return render(request, 'menu/create_order.html', {'pizzas': pizzas})

def order_detail_view(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'menu/order_detail.html', {'order': order})

def  get_pizzas(request):
    get_pizzas=Pizza.objects.all()
    return render (request,'menu/menu.html', {'all_pizzas': get_pizzas })
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Создаем нового пользователя
        user = User.objects.create_user(username=username, email=email, password=password)

        # Автоматически логиним пользователя после регистрации
        login(request, user)

        # Перенаправляем на главную страницу после регистрации
        return redirect('menu')

    return render(request, 'register.html')

def index(request):
    pizzas = Pizza.objects.all()  # Получаем все пиццы из базы данных
    context = {'pizzas': pizzas}
    return render(request, 'index.html', context)

def about_us(request):
    return render(request, 'about-us.html')

def typography(request):
    return render(request, 'typography.html')

def contacts(request):
    return render(request, 'contacts.html')

def menu(request):
    return render(request, 'menu.html')

def create_order(request):
    if request.method == 'POST':
        customer = request.POST.get('customer')
        pizza_id = request.POST.get('pizza')
        quantity = int(request.POST.get('quantity'))

        pizza = Pizza.objects.get(id=pizza_id)
        order = Order.objects.create(customer=customer)
        OrderItem.objects.create(order=order, pizza=pizza, quantity=quantity)

        return redirect('order_detail', order_id=order.id)  # Перенаправление на страницу деталей заказа

    pizzas = Pizza.objects.all()
    context = {'pizzas': pizzas}
    return render(request, 'create_order.html', context)

def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    context = {'order': order}
    return render(request, 'order_detail.html', context)