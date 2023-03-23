from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import *
from .forms import *


# Главная страница
def index(request):
    return render(request, 'index.html')


# Регистрация
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'register.html'

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.save()
            return redirect('home')
        else:
            print('WHY')
            return render(request, self.template_name, {'form': form})


# Вход
class LoginUser(LoginView):
    form_class = CustomUserLoginForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('home')


# Создание заказа
def make_order(request):
    if request.user.is_authenticated:
        order = Order.objects.create(user=request.user)
        return redirect(order.get_absolute_url())
    else:
        return redirect('login')


# Карточка заказа для пользователя
def show_order(request, order_id):
    if not request.user.is_authenticated:
        return redirect('login')
    order = Order.objects.get(pk=order_id)
    if request.user != order.user:
        return redirect('home')
    if not request.user.is_authenticated:
        redirect('register')
    if request.method == 'POST':
        form = MakeProductForm(request.POST)
        if form.is_valid():
            Product.objects.create(**form.cleaned_data, order=order)
            return redirect(order.get_absolute_url())
    else:
        form = MakeProductForm
    return render(request, 'show_order.html', {'order': order, 'form': form})


# Вспомогательная функция удаления товара
def delete_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    order = product.order
    if request.user == order.user and request.user.is_authenticated:
        product.delete()
        return redirect(order.get_absolute_url())
    else:
        return redirect('home')


# Список заказов клиента
def my_orders_list(request):
    if request.user.is_authenticated:
        return render(request, 'my_orders_list.html')
    else:
        return redirect('login')


# Вспомогательная функция удаления заказа
def delete_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    if request.user == order.user and request.user.is_authenticated:
        Order.objects.get(pk=order_id).delete()
        return redirect('my_orders_list')
    else:
        return redirect('home')


# Список заказов для проверки администратором
def orders_list(request):
    if request.user.is_staff:
        Orders = Order.objects.all()
        return render(request, 'orders_list.html', {'Orders': Orders})
    else:
        return redirect('home')


# Карточка заказа для проверки администратором
def order_check(request, order_id):
    order = Order.objects.get(pk=order_id)
    if not request.user.is_staff:
        return redirect('home')
    if not request.user.is_authenticated:
        redirect('register')
    if request.method == 'POST':
        form = MakeStatusForm(request.POST)
        if form.is_valid():
            Status.objects.create(**form.cleaned_data, order=order, admin=request.user)
            return redirect(order.get_check_url())
    else:
        form = MakeStatusForm
    return render(request, 'order_check.html', {'order': order, 'form': form})


# Выход
def logout_user(request):
    logout(request)
    return redirect('home')


# Вспомогательная функция удаления статуса заказа
def delete_status(request, status_id):
    status = Status.objects.get(pk=status_id)
    order = status.order
    if request.user.is_staff:
        status.delete()
        return redirect(order.get_check_url())
    else:
        return redirect('home')
