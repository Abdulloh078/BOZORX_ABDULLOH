from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Barcha e'lonlar va kategoriya bo'yicha saralash
    path('', views.product_list_view, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list_view, name='product_list_by_category'),
    
    # Yangi e'lon yaratish
    path('create/', views.product_create_view, name='product_create'),
    
    # E'lon uchun to'lov sahifasi (slug'lardan tepada turishi shart!)
    path('payment/<int:product_id>/', views.payment_page_view, name='payment_page'),
    
    # Yurakcha (Favorite) bosish uchun AJAX URL
    path('<slug:slug>/favorite/', views.toggle_favorite_view, name='toggle_favorite'),
    
    # Tahrirlash va O'chirish
    path('<slug:slug>/update/', views.product_update_view, name='product_update'),
    path('<slug:slug>/delete/', views.product_delete_view, name='product_delete'),
    
    # Mahsulot haqida batafsil sahifa (Eng oxirida bo'lgani ma'qul)
    path('<slug:slug>/', views.product_detail_view, name='product_detail'),
]