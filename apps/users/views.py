from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm  # Profilni tahrirlash formasi (pastroqda yaratamiz)

@login_required
def profile_view(request):
    """
    Foydalanuvchi profili va uning e'lonlari
    """
    user = request.user
    user_products = user.products.all()  # Foydalanuvchiga tegishli e'lonlar
    
    context = {
        'user': user,
        'products': user_products,
        'products_count': user_products.count(),
    }
    return render(request, 'users/profile.html', context)


@login_required
def profile_edit_view(request):
    """
    Profil ma'lumotlarini tahrirlash
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil ma'lumotlari muvaffaqiyatli yangilandi!")
            return redirect('users:profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'users/profile_edit.html', {'form': form})