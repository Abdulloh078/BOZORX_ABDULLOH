from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Product(models.Model):
    # Mavjud maydonlaringiz (sarlavha, narx, tavsif, rasm va h.k.)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # --- PULLIK VA MODERATSIYA MAYDONLARI ---
    is_paid = models.BooleanField(default=False, verbose_name="To'lov qilinganmi")
    is_approved = models.BooleanField(default=False, verbose_name="Admin tasdiqladimi")
    publication_fee = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=9000.00,  # Boshlanishiga 9 000 so'm
        verbose_name="E'lon narxi"
    )

    def __str__(self):
        return self.title