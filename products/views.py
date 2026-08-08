from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Product, Category
from .forms import ProductForm


def product_list(request):
    """
    Barcha e'lonlarni chiqarish va sahifalarga bo'lish (Paginatsiya)
    """
    products_list = Product.objects.all().order_by('-id')

    # Filtr bor-yo'qligini tekshirish
    condition = request.GET.get('condition')
    if condition:
        products_list = products_list.filter(condition=condition)

    # SHU YERDA: 1 sahifada 10 ta e'lon (tekshirish uchun 2 yoki 3 qo'yib ko'rishingiz mumkin)
    paginator = Paginator(products_list, 10) 
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'products': page_obj,      # HTML dagi {% for product in products %} uchun
        'page_obj': page_obj,      # Paginatsiya tugmalari uchun
        'is_paginated': page_obj.has_other_pages(),
        'categories': categories,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    """
    Mahsulot batafsil sahifasi
    """
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'products/product_detail.html', {'product': product})


@login_required
def product_create(request):
    """
    Yangi e'lon qo'shish
    """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            
            # Modellaringizdagi maydonga qarab biri ishlatiladi
            if hasattr(product, 'seller'):
                product.seller = request.user
            elif hasattr(product, 'user'):
                product.user = request.user
            
            # Dinamik kiritilgan qo'shimcha maydonlarni yig'ish
            extra_details = []
            cleaned = form.cleaned_data
            
            # Avto
            if cleaned.get('auto_year'): extra_details.append(f"Yili: {cleaned['auto_year']}")
            if cleaned.get('auto_mileage'): extra_details.append(f"Bosgan masofasi: {cleaned['auto_mileage']} km")
            if cleaned.get('auto_fuel'): extra_details.append(f"Yoqilg'i: {cleaned['auto_fuel']}")
            if cleaned.get('auto_transmission'): extra_details.append(f"Uzatmalar qutisi: {cleaned['auto_transmission']}")
            
            # Texnika
            if cleaned.get('tech_brand'): extra_details.append(f"Brend: {cleaned['tech_brand']}")
            if cleaned.get('tech_memory'): extra_details.append(f"Xotira: {cleaned['tech_memory']}")
            if cleaned.get('tech_color'): extra_details.append(f"Rang: {cleaned['tech_color']}")
            
            # Kitob
            if cleaned.get('book_author'): extra_details.append(f"Muallif: {cleaned['book_author']}")
            if cleaned.get('book_genre'): extra_details.append(f"Janr: {cleaned['book_genre']}")

            # Qo'shimcha ma'lumotlarni tavsifga qo'shish
            if extra_details:
                existing_desc = product.description or ""
                product.description = existing_desc + "\n\n--- Qo'shimcha ma'lumotlar ---\n" + "\n".join(extra_details)

            product.save()
            return redirect('products:product_list')
    else:
        form = ProductForm()

    return render(request, 'products/product_create.html', {'form': form})