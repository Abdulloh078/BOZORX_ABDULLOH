from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Barcha e'lonlar va filtrlash
    path('', views.product_list_view, name='product_list'),
    
    # Kategoriya bo'yicha saralash
    path('category/<slug:category_slug>/', views.product_list_view, name='product_list_by_category'),
    
    # Yangi e'lon yaratish
    path('create/', views.product_create_view, name='product_create'),

    # SAVAT (CART) BO'LIMI
    path('cart/', views.cart_detail_view, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add_view, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove_view, name='cart_remove'),
    
    # Yurakcha (Favorite) bosish uchun AJAX
    path('<slug:slug>/favorite/', views.toggle_favorite_view, name='toggle_favorite'),
    
    # Tahrirlash va O'chirish
    path('<slug:slug>/update/', views.product_update_view, name='product_update'),
    path('<slug:slug>/delete/', views.product_delete_view, name='product_delete'),
    
    # Mahsulot haqida batafsil (Har doim dynamik slug URL-lar oxirida bo'lishi kerak)
    path('<slug:slug>/', views.product_detail_view, name='product_detail'),


]