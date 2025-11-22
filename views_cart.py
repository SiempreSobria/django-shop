from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .cart import Cart
from .models import Product

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product_id)
    
    # Если это AJAX запрос, возвращаем JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total_items': cart.get_total_quantity(),
            'message': f'{product.title} добавлен в корзину'
        })
    
    # Иначе обычный редирект
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    
    # Если это AJAX запрос, возвращаем JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total_items': cart.get_total_quantity(),
            'message': 'Товар удален из корзины'
        })
    
    return redirect('cart_detail')

# ДОБАВЬТЕ ЭТУ ФУНКЦИЮ
@require_POST
def cart_update(request, product_id):
    """
    Обновление количества товара в корзине
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    try:
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity <= 0:
            cart.remove(product_id)
            message = f'{product.title} удален из корзины'
        else:
            cart.add(product_id, quantity=quantity, update_quantity=True)
            message = f'Количество {product.title} обновлено'
        
        # Если это AJAX запрос, возвращаем JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_total_items': cart.get_total_quantity(),
                'cart_total_price': str(cart.get_total_price()),
                'product_quantity': quantity if quantity > 0 else 0,
                'message': message
            })
        
        return redirect('cart_detail')
        
    except Exception as e:
        print(f"Error updating cart: {e}")
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'Ошибка при обновлении корзины'
            }, status=400)
        
        return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart_detail.html', {'cart': cart})