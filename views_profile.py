from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def profile(request):
    return render(request, 'shop/profile.html')

@login_required
def my_orders(request):
    """Страница с заказами пользователя"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/my_orders.html', {'orders': orders})