from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify


class Category(models.Model):
    """
    Iyerarxik Kategoriya Modeli (Parent-Child)
    """
    name = models.CharField('Kategoriya nomi', max_length=100)
    slug = models.SlugField('URL Slug', unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='Ota kategoriya')
    icon = models.CharField('FontAwesome/Bootstrap Ikonka sinfi', max_length=50, blank=True, help_text="Masalan: bi bi-laptop")
    image = models.ImageField('Kategoriya rasmi', upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])


class Product(models.Model):
    """
    Marketplace E'lonlar/Mahsulotlar Modeli
    """
    class Condition(models.TextChoices):
        NEW = 'NEW', 'Yangi'
        USED = 'USED', 'Ishlatilgan'
        REFURBISHED = 'REFURBISHED', 'Tiklangani (Refurbished)'

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Qoralama'
        PENDING = 'PENDING', 'Tekshiruvda (Moderatsiya)'
        ACTIVE = 'ACTIVE', 'Faol'
        REJECTED = 'REJECTED', 'Radd etilgan'
        SOLD = 'SOLD', 'Sotilgan'

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products', verbose_name='Sotuvchi')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products', verbose_name='Kategoriya')
    title = models.CharField('E\'lon sarlavhasi', max_length=255)
    slug = models.SlugField('URL Slug', max_length=255, unique=True, blank=True)
    description = models.TextField('Batafsil tavsif')
    price = models.DecimalField('Narxi (so\'m)', max_digits=12, decimal_places=2)
    is_negotiable = models.BooleanField('Kelishtiriladi', default=False)
    
    phone_number = models.CharField('Aloqa uchun tel. raqam', max_length=20, blank=True, null=True, help_text="Masalan: +998901234567")

    condition = models.CharField('Holati', max_length=20, choices=Condition.choices, default=Condition.USED)
    status = models.CharField('E\'lon holati', max_length=20, choices=Status.choices, default=Status.PENDING)
    
    # Joylashuv
    region = models.CharField('Viloyat', max_length=100)
    city = models.CharField('Tuman / Shahar', max_length=100)
    
    # Reklama statuslari (Top / VIP)
    is_vip = models.BooleanField('VIP e\'lon', default=False)
    is_top = models.BooleanField('TOP e\'lon', default=False)
    views_count = models.PositiveIntegerField('Ko\'rishlar soni', default=0)

    created_at = models.DateTimeField('Yaratilgan vaqti', auto_now_add=True)
    updated_at = models.DateTimeField('Yangilangan vaqti', auto_now=True)

    class Meta:
        verbose_name = 'Mahsulot / E\'lon'
        verbose_name_plural = 'Mahsulotlar va E\'lonlar'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            count = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    """
    Mahsulotning ko'p sonli rasmlari
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Mahsulot')
    image = models.ImageField('Rasm', upload_to='products/%Y/%m/')
    is_main = models.BooleanField('Asosiy rasm', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mahsulot rasmi'
        verbose_name_plural = 'Mahsulot rasmlari'


class Review(models.Model):
    """
    Mahsulotga qoldirilgan izoh va baho (Rating)
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Mahsulot')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews', verbose_name='Foydalanuvchi')
    rating = models.PositiveSmallIntegerField('Baho', default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField('Izoh')
    created_at = models.DateTimeField('Yaratilgan vaqti', auto_now_add=True)

    class Meta:
        verbose_name = 'Izoh va Baho'
        verbose_name_plural = 'Izohlar va Baholar'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.product.title} ({self.rating}★)"


class Favorite(models.Model):
    """
    Saralangan (Yoqtirilgan) e'lonlar
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites', verbose_name='Foydalanuvchi')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by', verbose_name='Mahsulot')
    created_at = models.DateTimeField('Qo\'shilgan vaqti', auto_now_add=True)

    class Meta:
        verbose_name = 'Saralangan e\'lon'
        verbose_name_plural = 'Saralangan e\'lonlar'
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user} -> {self.product.title}"