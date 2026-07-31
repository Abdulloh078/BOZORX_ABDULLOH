from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm
from .models import User, UserProfile


def register_view(request):
    # Agar foydalanuvchi allaqachon tizimga kirgan bo'lsa, bosh sahifaga yuboriladi
    if request.user.is_authenticated:
        return redirect('products:product_list')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)  # Avtomatik profil yaratish
            
            # Ro'yxatdan o'tgandan so'ng darhol login sahifasiga yuborish
            messages.success(request, "Muvaffaqiyatli ro'yxatdan o'tdingiz! Endi tizimga kiring.")
            return redirect('accounts:login')
        else:
            messages.error(request, "Xatolik yuz berdi. Ma'lumotlarni tekshirib qayta kiriting.")
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    # Agar foydalanuvchi allaqachon tizimga kirgan bo'lsa, bosh sahifaga yuboriladi
    if request.user.is_authenticated:
        return redirect('products:product_list')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Qaytganingizdan xursandmiz, {user.username}!")
            return redirect(request.GET.get('next') or 'products:product_list')
        else:
            messages.error(request, "Login yoki parol noto'g'ri.")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Siz tizimdan chiqdingiz.")
    # Chiqib ketganda ham Login sahifasiga yuboramiz
    return redirect('accounts:login')


@login_required
def profile_view(request):
    """
    Foydalanuvchining shaxsiy kabinet sahifasi
    """
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    context = {
        'profile': profile
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit_view(request):
    """
    Foydalanuvchi profilini va shaxsiy ma'lumotlarini tahrirlash sahifasi
    """
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profil ma'lumotlaringiz muvaffaqiyatli yangilandi!")
            return redirect('accounts:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile': profile
    }
    return render(request, 'accounts/profile_edit.html', context)


def seller_store_view(request, username):
    """
    Sotuvchining shaxsiy do'kon sahifasi: example.com/store/abdulloh
    """
    seller = get_object_or_404(User, username=username)
    profile, _ = UserProfile.objects.get_or_create(user=seller)
    
    context = {
        'seller': seller,
        'profile': profile,
    }
    return render(request, 'accounts/seller_store.html', context)