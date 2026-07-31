from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apps.products.models import Product
from .models import Dialog, Message

@login_required
def start_dialog_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.seller == request.user:
        return redirect('products:product_detail', slug=product.slug)

    dialog, created = Dialog.objects.get_or_create(
        product=product,
        sender=request.user,
        recipient=product.seller
    )
    return redirect('chat:dialog_detail', dialog_id=dialog.id)

@login_required
def dialog_list_view(request):
    dialogs = Dialog.objects.filter(sender=request.user) | Dialog.objects.filter(recipient=request.user)
    return render(request, 'chat/dialog_list.html', {'dialogs': dialogs.distinct()})

@login_required
def dialog_detail_view(request, dialog_id):
    dialog = get_object_or_404(Dialog, id=dialog_id)
    if request.user not in [dialog.sender, dialog.recipient]:
        return redirect('chat:dialog_list')

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Message.objects.create(dialog=dialog, sender=request.user, text=text)
            return redirect('chat:dialog_detail', dialog_id=dialog.id)

    messages_qs = dialog.messages.all()
    return render(request, 'chat/dialog_detail.html', {'dialog': dialog, 'chat_messages': messages_qs})