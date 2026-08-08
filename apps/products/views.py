from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from .models import Product, Category, ProductImage, Review, Favorite
from .forms import ProductForm, ReviewForm


def get_all_subcategory_ids(category):
    """
    Kategoriya va uning BARCHA ichki ost-kategoriyalari (children/subcategories) ID larini yig'ib beradi.
    """
    category_ids = [category.id]
    children = category.children.all()
    for child in children:
        category_ids.extend(get_all_subcategory_ids(child))
    return category_ids


def product_list_view(request, category_slug=None):
    """
    Barcha e'lonlar, kategoriyalar, qidiruv va foydalanuvchi e'lonlarini ko'rsatuvchi view
    """
    category = None
    categories = Category.objects.filter(parent=None)
    products = Product.objects.filter(status=Product.Status.ACTIVE).select_related('category', 'seller').prefetch_related('images')

    # 1. "Mening E'lonlarim" filtri (?my_products=1)
    my_products = request.GET.get('my_products')
    if my_products == '1':
        if request.user.is_authenticated:
            products = products.filter(seller=request.user)
        else:
            messages.info(request, "O'zingizning e'lonlaringizni ko'rish uchun tizimga kiring!")
            return redirect('accounts:login')

    # 2. Kategoriya va uning BARCHA ost-kategoriyalari bo'yicha filter
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        all_cat_ids = get_all_subcategory_ids(category)
        products = products.filter(category_id__in=all_cat_ids)

    # 3. Qidiruv paneli filtri (?q=query)
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # 4. Holati bo'yicha filter (NEW, USED, REFURBISHED)
    condition = request.GET.get('condition')
    if condition:
        products = products.filter(condition=condition)

    # Foydalanuvchining saralangan (yoqtirgan) e'lonlari ID lari
    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'selected_condition': condition,
        'query': query,
        'user_favorites': user_favorites,
        'is_my_products': my_products == '1',
    }
    return render(request, 'products/product_list.html', context)


def product_detail_view(request, slug):
    """
    Mahsulotning batafsil sahifasi
    """
    product = get_object_or_404(Product, slug=slug)

    # Ko'rishlar sonini oshirish
    product.views_count += 1
    product.save(update_fields=['views_count'])

    # POST so'rovi kelganda (izoh/baho qoldirilganda)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, "Izoh qoldirish uchun tizimga kiring!")
            return redirect('accounts:login')

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Izohingiz muvaffaqiyatli saqlandi!")
            return redirect('products:product_detail', slug=product.slug)
        else:
            messages.error(request, "Izoh saqlashda xatolik yuz berdi. Shaklni to'g'ri to'ldiring!")
    else:
        form = ReviewForm()

    # Izohlar va o'rtacha baho
    reviews = product.reviews.select_related('user').all().order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    # O'xshash mahsulotlar
    related_products = Product.objects.filter(
        category=product.category, 
        status=Product.Status.ACTIVE
    ).exclude(id=product.id).prefetch_related('images')[:4]

    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'related_products': related_products,
        'form': form,
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def toggle_favorite_view(request, slug):
    """
    Yurakcha (Favorite) bosilganda ishlaydigan AJAX view
    """
    if request.method == 'POST':
        product = get_object_or_404(Product, slug=slug)
        favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)

        if not created:
            favorite.delete()
            is_favorite = False
        else:
            is_favorite = True

        return JsonResponse({'is_favorite': is_favorite})

    return JsonResponse({'error': "Noto'g'ri so'rov"}, status=400)


@login_required
def product_create_view(request):
    """
    Yangi e'lon qo'shish
    """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')

        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            
            # Dinamik maydonlarni xaritalash
            data = form.cleaned_data
            fields_map = [
                ('auto_year', '📅 Chiqarilgan yili'),
                ('auto_mileage', '🛣️ Yurgan masofasi', lambda v: f"{v:,} km"),
                ('auto_fuel', '⛽ Yoqilg\'i turi', lambda v: dict(form.fields['auto_fuel'].choices).get(v, v)),
                ('auto_transmission', '⚙️ Korobka', lambda v: dict(form.fields['auto_transmission'].choices).get(v, v)),
                ('tech_brand', '🏷️ Brend/Marka'),
                ('tech_memory', '💾 Xotira'),
                ('tech_color', '🎨 Rangi'),
                ('home_rooms', '🚪 Xonalar soni'),
                ('home_area', '📐 Maydoni'),
                ('home_floor', '🏢 Qavat'),
                ('food_weight', '⚖️ Og\'irligi/Hajmi'),
                ('food_expiry', '⏳ Yaroqlilik muddati'),
                ('clothing_size', '📏 O\'lchami (Razmer)'),
                ('clothing_gender', '👤 Kim uchun', lambda v: dict(form.fields['clothing_gender'].choices).get(v, v)),
                ('furniture_material', '🪵 Materiali'),
                ('service_type', '🛠️ Xizmat turi'),
                ('pet_age', '🐾 Yoshi/Zoti'),
                ('job_salary', '💵 Oylik maosh'),
                ('job_type', '⏰ Ish grafigi', lambda v: dict(form.fields['job_type'].choices).get(v, v)),
                ('sport_category', '⚽ Sport turi'),
            ]

            extra_info = ""
            for item in fields_map:
                field_name = item[0]
                label = item[1]
                formatter = item[2] if len(item) > 2 else None
                
                val = data.get(field_name)
                if val is not None and val != '':
                    formatted_val = formatter(val) if formatter else str(val)
                    extra_info += f"\n{label}: {formatted_val}"

            if extra_info:
                product.description = (product.description or '') + "\n\n📋 --- Xarakteristikalar ---" + extra_info

            product.status = Product.Status.ACTIVE
            product.save()

            for index, image in enumerate(images):
                ProductImage.objects.create(
                    product=product, 
                    image=image, 
                    is_main=(index == 0)
                )

            messages.success(request, "E'loningiz muvaffaqiyatli joylandi!")
            return redirect('products:product_detail', slug=product.slug)
        else:
            messages.error(request, "Iltimos, shakldagi xatoliklarni to'g'rilang.")
    else:
        form = ProductForm()

    return render(request, 'products/product_create.html', {'form': form})


@login_required
def product_update_view(request, slug):
    """
    E'lonni tahrirlash sahifasi
    """
    product = get_object_or_404(Product, slug=slug)

    if product.seller != request.user:
        raise PermissionDenied("Siz faqat o'zingizning e'loningizni tahrirlashingiz mumkin!")

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        images = request.FILES.getlist('images')

        if form.is_valid():
            product = form.save()

            if images:
                for index, image in enumerate(images):
                    is_main_flag = (index == 0 and not product.images.filter(is_main=True).exists())
                    ProductImage.objects.create(
                        product=product,
                        image=image,
                        is_main=is_main_flag
                    )

            messages.success(request, "E'loningiz muvaffaqiyatli tahrirlandi!")
            return redirect('products:product_detail', slug=product.slug)
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_create.html', {
        'form': form, 
        'product': product,
        'is_edit': True
    })


@login_required
def product_delete_view(request, slug):
    """
    E'lonni o'chirish sahifasi
    """
    product = get_object_or_404(Product, slug=slug)

    if product.seller != request.user:
        raise PermissionDenied("Siz faqat o'zingizning e'loningizni o'chira olasiz!")

    if request.method == 'POST':
        product.delete()
        messages.success(request, "E'lon muvaffaqiyatli o'chirib tashlandi!")
        return redirect('products:product_list')

    return render(request, 'products/product_confirm_delete.html', {'product': product})


# ==========================================
# SAVAT (CART) BO'LIMI FUNKSIYALARI
# ==========================================

def cart_detail_view(request):
    """
    Savatdagi mahsulotlarni va sotuvchi ma'lumotlarini ko'rsatish
    """
    cart = request.session.get('cart', {})
    product_ids = [int(pid) for pid in cart.keys() if str(pid).isdigit()]
    
    # Sotuvchi ma'lumotlarini shablonda xatolarsiz ko'rsatish uchun select_related('seller') qo'shildi
    products_db = Product.objects.filter(id__in=product_ids).select_related('seller').prefetch_related('images')
    
    cart_items = []
    total_sum = 0

    for product in products_db:
        quantity = cart.get(str(product.id), 0)
        total_price = product.price * quantity
        total_sum += total_price
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price,
        })

    context = {
        'cart_items': cart_items,
        'total_sum': total_sum,
    }
    return render(request, 'products/cart_detail.html', context)


def cart_add_view(request, product_id):
    """
    Savatga mahsulot qo'shish
    """
    cart = request.session.get('cart', {})
    str_id = str(product_id)
    
    cart[str_id] = cart.get(str_id, 0) + 1
    
    request.session['cart'] = cart
    request.session.modified = True
    
    return redirect(request.META.get('HTTP_REFERER', 'products:cart_detail'))


def cart_remove_view(request, product_id):
    """
    Savatdan mahsulotni o'chirish
    """
    cart = request.session.get('cart', {})
    str_id = str(product_id)
    
    if str_id in cart:
        del cart[str_id]
        request.session['cart'] = cart
        request.session.modified = True
        
    return redirect('products:cart_detail')