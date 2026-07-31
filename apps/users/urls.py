from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # ... boshqa url-lar (login, register va h.k.)
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
]