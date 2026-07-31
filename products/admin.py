# products/admin.py
from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price', 'publication_fee', 'is_paid', 'is_approved', 'created_at')
    list_filter = ('is_paid', 'is_approved', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    list_editable = ('is_paid', 'is_approved', 'publication_fee') # Admin ro'yxatning o'zidanoq tasdiqlashi va narxni o'zgartirishi mumkin

    # Bir nechta e'lonni tanlab bittada tasdiqlash tugmasi
    actions = ['approve_products']

    def approve_products(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Tanlangan e'lonlar muvaffaqiyatli tasdiqlandi!")
    approve_products.short_description = "Tanlangan e'lonlarni tasdiqlash"