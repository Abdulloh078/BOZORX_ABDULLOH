from django.contrib import admin
from .models import Product, Category, ProductImage, Review, Favorite

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Modelingizda mavjud bo'lgan maydonlar:
    list_display = ('title', 'seller', 'price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description', 'seller__username')
    actions = ['approve_products']

    @admin.action(description="Tanlangan e'lonlarni faollashtirish (ACTIVE qilish)")
    def approve_products(self, request, queryset):
        queryset.update(status=Product.Status.ACTIVE)

# Agar bu modellar allaqachon boshqa joyda admin.site.register qilinmagan bo'lsa:
try:
    admin.site.register(Category)
    admin.site.register(ProductImage)
    admin.site.register(Review)
    admin.site.register(Favorite)
except admin.sites.AlreadyRegistered:
    pass