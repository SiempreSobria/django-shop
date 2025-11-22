from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, Product
from .cart import Cart


def order_create(request):
    """Создание заказа на основе корзины"""
    cart = Cart(request)

    # Корзина пуста
    if len(cart) == 0:
        messages.warning(request, "Ваша корзина пуста.")
        return redirect('products_list')

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        comment = request.POST.get("comment", "").strip()

        # Проверка обязательных полей
        if not name or not phone or not address:
            messages.error(request, "Пожалуйста, заполните обязательные поля.")
            return render(request, "shop/order_create.html", {"cart": cart})


        #     ВАЛИДАЦИЯ ТЕЛЕФОНА
        phone_clean = phone.replace("+", "").replace(" ", "").replace("-", "")

        if not phone_clean.isdigit():
            messages.error(request, "Телефон должен содержать только цифры (кроме +).")
            return render(request, 'shop/order_create.html', {'cart': cart})

        if len(phone_clean) != 11:
            messages.error(request, "Телефон должен содержать ровно 11 цифр.")
            return render(request, 'shop/order_create.html', {'cart': cart})

        if not (phone.startswith("+7") or phone.startswith("8") or phone_clean.startswith("7")):
            messages.error(request, "Телефон должен начинаться с +7 или 8.")
            return render(request, 'shop/order_create.html', {'cart': cart})

        # Создание заказа
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            name=name,
            phone=phone,
            address=address,
            comment=comment,
        )

        # Создание позиций
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                product_title=item["product"].title,
                price=item["price"],
                quantity=item["quantity"],
            )

        # Очистка корзины
        cart.clear()

        return redirect("order_success", order_id=order.id)

    # страница оформления
    return render(request, "shop/order_create.html", {"cart": cart})


def order_success(request, order_id):
    """Страница успешного заказа"""
    order = get_object_or_404(Order, id=order_id)

    if request.user.is_authenticated and order.user and order.user != request.user:
        messages.error(request, "У вас нет доступа к этому заказу.")
        return redirect('products_list')

    return render(request, "shop/order_success.html", {"order_id": order_id})
