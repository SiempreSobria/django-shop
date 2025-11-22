from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, views_cart, views_order, views_profile
from .auth_views import register

urlpatterns = [
    path('', views.products_list, name='products_list'),
    path('category/<slug:category_slug>/', views.products_list, name='products_by_category'),

    # Products
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),


    # Cart
    path('cart/', views_cart.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views_cart.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views_cart.cart_remove, name='cart_remove'),
    path('cart/update/<int:product_id>/', views_cart.cart_update, name='cart_update'),

    # Orders
    path('order/create/', views_order.order_create, name='order_create'),
    path('order/success/<int:order_id>/', views_order.order_success, name='order_success'),

    # Register
    path('register/', register, name='register'),

    # Profile
    path('accounts/profile/', views_profile.profile, name='profile'),
    path('accounts/orders/', views_profile.my_orders, name='my_orders'),


    # Auth
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    #Info
    path('about/', views.about, name='about'),
    path('delivery/', views.delivery, name='delivery'),
    path('contacts/', views.contacts, name='contacts'),   
]
