from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


phone_regex = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Telefon raqami '+998901234567' formatida bo'lishi kerak."
)

class User(AbstractUser):
    """
    Marketplace uchun kengaytirilgan Custom User modeli.
    """
    class UserType(models.TextChoices):
        BUYER = 'BUYER', 'Xaridor'
        SELLER = 'SELLER', 'Sotuvchi'
        MODERATOR = 'MODERATOR', 'Moderator'
        ADMIN = 'ADMIN', 'Admin'

    email = models.EmailField('Email manzil', unique=True)
    phone = models.CharField('Telefon raqam', validators=[phone_regex], max_length=13, unique=True, null=True, blank=True)
    user_type = models.CharField('Foydalanuvchi turi', max_length=20, choices=UserType.choices, default=UserType.BUYER)
    is_verified = models.BooleanField('Tasdiqlangan foydalanuvchi', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_full_name() or self.email})"


class UserProfile(models.Model):
    """
    Sotuvchi do'koni va qo'shimcha profil ma'lumotlari.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField('Profil rasmi', upload_to='avatars/%Y/%m/', default='avatars/default.png', blank=True)
    bio = models.TextField('O\'zi haqida / Do\'kon tavsifi', max_length=500, blank=True)
    region = models.CharField('Viloyat', max_length=100, blank=True)
    city = models.CharField('Tuman / Shahar', max_length=100, blank=True)
    address = models.CharField('Aniq manzil', max_length=255, blank=True)
    balance = models.DecimalField('Hisob balansi (so\'m)', max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} profili"