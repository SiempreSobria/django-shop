from decimal import Decimal
from django.shortcuts import get_object_or_404
from .models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product_id, quantity=1, update_quantity=False):
        """
        Добавить товар в корзину или обновить его количество
        """
        product = get_object_or_404(Product, id=product_id)
        pid = str(product_id)
        
        if pid not in self.cart:
            self.cart[pid] = {
                'quantity': 0, 
                'price': str(product.price),
                'product_title': product.title  # Сохраняем название для сообщений
            }
        
        if update_quantity:
            self.cart[pid]['quantity'] = int(quantity)
        else:
            self.cart[pid]['quantity'] += int(quantity)
            
        # Гарантируем, что количество не отрицательное
        if self.cart[pid]['quantity'] <= 0:
            self.remove(product_id)
        else:
            self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product_id):
        """
        Удалить товар из корзины
        """
        pid = str(product_id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def get_product_quantity(self, product_id):
        """
        Получить количество конкретного товара в корзине
        """
        pid = str(product_id)
        if pid in self.cart:
            return self.cart[pid]['quantity']
        return 0

    def __iter__(self):
        """
        Итератор по товарам в корзине
        """
        product_ids = list(self.cart.keys())
        products = Product.objects.filter(id__in=product_ids)
        prod_map = {str(p.id): p for p in products}
        
        for pid, item in self.cart.items():
            product = prod_map.get(pid)
            if not product:
                continue
            item_data = {
                'product': product,
                'quantity': item['quantity'],
                'price': Decimal(item['price']),
                'product_title': item.get('product_title', product.title)
            }
            item_data['total_price'] = item_data['price'] * item_data['quantity']
            yield item_data

    def __len__(self):
        """
        Общее количество позиций в корзине (уникальные товары)
        """
        return len(self.cart)

    def get_total_quantity(self):
        """
        Общее количество товаров (все единицы)
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Общая стоимость корзины
        """
        try:
            return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
        except (KeyError, Decimal.InvalidOperation):
            return Decimal('0')

    def get_item_total_price(self, product_id):
        """
        Получить общую стоимость для конкретного товара
        """
        pid = str(product_id)
        if pid in self.cart:
            try:
                return Decimal(self.cart[pid]['price']) * self.cart[pid]['quantity']
            except (KeyError, Decimal.InvalidOperation):
                return Decimal('0')
        return Decimal('0')

    def clear(self):
        """
        Очистить корзину
        """
        self.session['cart'] = {}
        self.save()

    def is_empty(self):
        """
        Проверить, пуста ли корзина
        """
        return len(self.cart) == 0

    def get_cart_items_count(self):
        """
        Количество уникальных товаров в корзине (алиас для len)
        """
        return len(self.cart)

    def to_dict(self):
        """
        Представление корзины в виде словаря для JSON ответов
        """
        return {
            'total_quantity': self.get_total_quantity(),
            'total_price': str(self.get_total_price()),
            'items_count': self.get_cart_items_count(),
            'items': [
                {
                    'product_id': pid,
                    'quantity': item['quantity'],
                    'price': item['price'],
                    'product_title': item.get('product_title', '')
                }
                for pid, item in self.cart.items()
            ]
        }