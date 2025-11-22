from .models import Category
from .cart import Cart

def categories(request):
    return {
        'categories': Category.objects.all()
    }

def cart(request):
    """Контекстный процессор для корзины"""
    return {'cart': Cart(request)}

def categories_processor(request):
    """
    Возвращает список категорий для navbar.
    Если категорий нет, вернёт пустой QuerySet.
    """
    return {'categories': Category.objects.all()}