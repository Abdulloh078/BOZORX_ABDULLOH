from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.products.models import Product
from .models import Dialog, Message


@login_required
def start_dialog_view(request, product_id):
    """
    Sotuvchi va xaridor o'rtasida chat boshlash yoki mavjud muloqotga o'tish
    """
    # Mahsulot bazada yo'q bo'lsa 404 o'rniga xabar berib ortga qaytarish
    product = Product.objects.filter(id=product_id).first()
    
    if not product:
        messages.error(request, "Afsuski, ushbu e'lon topilmadi yoki o'chirib tashlangan!")
        return redirect('products:product_list')

    # Foydalanuvchi o'z e'loniga chat ocha olmaydi
    if product.seller == request.user:
        messages.warning(request, "O'zingizning e'loningiz bo'yicha oz-o'zingizga xabar yubora olmaysiz!")
        return redirect('products:product_detail', slug=product.slug)

    # Dialogni olish yoki yangisini yaratish
    dialog, created = Dialog.objects.get_or_create(
        product=product,
        sender=request.user,
        recipient=product.seller
    )
    
    return redirect('chat:dialog_detail', dialog_id=dialog.id)


@login_required
def dialog_list_view(request):
    """
    Foydalanuvchining barcha chatlar ro'yxati
    """
    dialogs = (Dialog.objects.filter(sender=request.user) | Dialog.objects.filter(recipient=request.user)).distinct()
    
    return render(request, 'chat/dialog_list.html', {
        'dialogs': dialogs
    })


@login_required
def dialog_detail_view(request, dialog_id):
    """
    Alohida chat sahifasi va xabarlashuv
    """
    dialog = get_object_or_404(Dialog, id=dialog_id)

    # Begona foydalanuvchilar chatga kira olmasligini ta'minlash
    if request.user not in [dialog.sender, dialog.recipient]:
        messages.error(request, "Ushbu suhbatni ko'rish uchun sizda ruxsat yo'q!")
        return redirect('chat:dialog_list')

    # Yangi xabar yuborilganda
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            Message.objects.create(
                dialog=dialog,
                sender=request.user,
                text=text
            )
            return redirect('chat:dialog_detail', dialog_id=dialog.id)

    # Xabarlarni xronologik tartibda olish
    messages_qs = dialog.messages.all().order_by('created_at') if hasattr(Message, 'created_at') else dialog.messages.all()

    context = {
        'dialog': dialog,
        'chat_messages': messages_qs,
    }
    return render(request, 'chat/dialog_detail.html', context)