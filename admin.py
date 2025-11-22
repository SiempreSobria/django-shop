from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'stock', 'preview')
    list_filter = ('category',)
    search_fields = ('title','description')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:100px; height:auto; object-fit:cover;" />', obj.image.url)
        return '(нет изображения)'
    preview.short_description = 'Превью'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product','price','quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','name','phone','created_at','total_items','total_price')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at',)

    def total_price(self, obj):
        return f"{obj.total_price()} ₽"
    total_price.short_description = 'Сумма'

    def total_items(self, obj):
        return obj.total_items()
    total_items.short_description = 'Кол-во'
