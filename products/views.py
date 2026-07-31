# products/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product

@login_required
def product_create(request):
    if request.method == 'POST':
        # Formadan ma'lumotlarni olish kodi...
        # Product ob'ektini yaratamiz
        product = Product.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            user=request.user,
            publication_fee=9000.00, # Hozircha 9000 so'm
            is_paid=False,
            is_approved=False
        )
        # To'lov sahifasiga yo'naltiramiz
        return redirect('products:payment_page', product_id=product.id)

    return render(request, 'products/product_create.html')

@login_required
def payment_page(request, product_id):
    product = get_object_or_404(Product, id=product_id, user=request.user)
    
    # Click, Payme yoki karta raqamiga o'tkazma usullarini ko'rsatish
    return render(request, 'products/payment.html', {'product': product})