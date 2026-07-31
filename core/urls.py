from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Bosh sahifaga (127.0.0.1:8000/) kirganda to'g'ridan-to'g'ri Login sahifasiga yo'naltiradi:
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    
    path('products/', include('apps.products.urls', namespace='products')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('chat/', include('apps.chat.urls', namespace='chat')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)