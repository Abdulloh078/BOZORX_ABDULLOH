from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.dialog_list_view, name='dialog_list'),
    path('start/<int:product_id>/', views.start_dialog_view, name='start_dialog'),
    path('<int:dialog_id>/', views.dialog_detail_view, name='dialog_detail'),
]