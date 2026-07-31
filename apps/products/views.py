from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from .models import Product, Category, ProductImage, Review, Favorite
from .forms import ProductForm, ReviewForm
from django.utils import timezone
from datetime import timedelta


def product_list_view(request, category_slug=None):
    """
    Barcha e'lonlar va kategoriyalar bo'yicha saralash sahifasi
    """
    category = None
    categories = Category.objects.filter(parent=None)
    products = Product.objects.filter(status=Product.Status.ACTIVE).select_related('category', 'seller').prefetch_related('images')

    # Kategoriya bo'yicha filter
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        sub_categories = category.children.all()
        categories_to_filter = [category] + list(sub_categories)
        products = products.filter(category__in=categories_to_filter)

    # Qidiruv
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # Holati bo'yicha filter (NEW, USED, REFURBISHED)
    condition = request.GET.get('condition')
    if condition:
        products = products.filter(condition=condition)

    # Tizimga kirgan foydalanuvchining yoqtirgan mahsulotlari ID larini olish
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
    }
    return render(request, 'products/product_list.html', context)


def product_detail_view(request, slug):
    """
    Mahsulotning batafsil sahifasi: 
    Ko'rishlar soni, izohlar, baholash va o'xshash mahsulotlarni ko'rsatadi
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

    # O'xshash mahsulotlar (xuddi shu kategoriyadagi 4 ta mahsulot)
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
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')

        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            
            # 1 oylik tekin yoki pullik shartni tekshirish (masalan, foydalanuvchining ilk e'loni tekin)
            user_products_count = Product.objects.filter(seller=request.user).count()
            if user_products_count == 0:
                # 1-oy tekin
                product.is_paid = True
                product.is_approved = True
                product.status = 'ACTIVE'
                product.save()
                messages.success(request, "Tabriklaymiz! 1 oylik tekin e'loningiz muvaffaqiyatli joylandi.")
                return redirect('products:product_detail', slug=product.slug)
            else:
                # Pullik e'lon (9000 so'm va to'lov sahifasiga o'tadi)
                product.is_paid = False
                product.is_approved = False
                product.status = 'INACTIVE'
                product.save()
                
                for index, image in enumerate(images):
                    ProductImage.objects.create(product=product, image=image, is_main=(index == 0))
                
                return redirect('products:payment_page', product_id=product.id)
    else:
        form = ProductForm()

    return render(request, 'products/product_create.html', {'form': form})


@login_required
def payment_page_view(request, product_id):
    """
    E'lon uchun to'lov sahifasi
    """
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    return render(request, 'products/payment.html', {'product': product})


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