from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def products_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/products_list.html', {'category': category, 'categories': categories, 'products': products})

def product_detail(request, slug):
    """
    Показывает страницу товара по slug
    """
    product = get_object_or_404(Product, slug=slug)

    similar = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'similar_products': similar,
    }
    return render(request, 'shop/product_detail.html', context)

#INFO
def about(request):
    return render(request, 'shop/about.html')

def delivery(request):
    return render(request, 'shop/delivery.html')

def contacts(request):
    return render(request, 'shop/contacts.html')
