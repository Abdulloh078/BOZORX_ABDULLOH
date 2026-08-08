from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Bosh sahifaga kirganda Login sahifasiga yo'naltiradi:
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    
    path('products/', include('apps.products.urls', namespace='products')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('chat/', include('apps.chat.urls', namespace='chat')),
]

# Local (DEBUG=True) va Render (DEBUG=False) rejimlari uchun media va static fayllar sozlamasi
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]