from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.urls import reverse


def generate_unique_slug(model_class, text, instance=None):
    """
    Kategoriya va Mahsulotlar uchun takrorlanmas (unique) slug generatsiya qiladi.
    """
    base_slug = slugify(text)
    if not base_slug:
        base_slug = 'item'
        
    slug = base_slug
    count = 1
    
    # Baza ichida ushbu slug mavjudligini tekshirish
    qs = model_class.objects.filter(slug=slug)
    if instance and instance.pk:
        qs = qs.exclude(pk=instance.pk)
        
    while qs.exists():
        slug = f"{base_slug}-{count}"
        qs = model_class.objects.filter(slug=slug)
        if instance and instance.pk:
            qs = qs.exclude(pk=instance.pk)
        count += 1
        
    return slug


class Category(models.Model):
    """
    Iyerarxik Kategoriya Modeli (Parent-Child)
    """
    name = models.CharField('Kategoriya nomi', max_length=100)
    slug = models.SlugField('URL Slug', max_length=120, unique=True, blank=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children', 
        verbose_name='Ota kategoriya'
    )
    icon = models.CharField('FontAwesome/Bootstrap Ikonka sinfi', max_length=50, blank=True, help_text="Masalan: bi bi-laptop")
    image = models.ImageField('Kategoriya rasmi', upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'
        ordering = ['name']

    def save(self, *args, **kwargs):
        # Slug bo'sh bo'lsa yoki nomi o'zgarganda avtomatik unikal slug beradi
        if not self.slug:
            self.slug = generate_unique_slug(Category, self.name, instance=self)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Kategoriya uchun avtomatik va xatosiz URL qaytaradi"""
        return reverse('products:product_list_by_category', kwargs={'category_slug': self.slug})

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
        ACTIVE = 'ACTIVE', 'Faol'
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
    status = models.CharField('E\'lon holati', max_length=20, choices=Status.choices, default=Status.ACTIVE)
    
    region = models.CharField('Viloyat', max_length=100)
    city = models.CharField('Tuman / Shahar', max_length=100)
    
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
            self.slug = generate_unique_slug(Product, self.title, instance=self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Mahsulot')
    image = models.ImageField('Rasm', upload_to='products/%Y/%m/')
    is_main = models.BooleanField('Asosiy rasm', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mahsulot rasmi'
        verbose_name_plural = 'Mahsulot rasmlari'


class Review(models.Model):
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites', verbose_name='Foydalanuvchi')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by', verbose_name='Mahsulot')
    created_at = models.DateTimeField('Qo\'shilgan vaqti', auto_now_add=True)

    class Meta:
        verbose_name = 'Saralangan e\'lon'
        verbose_name_plural = 'Saralangan e\'lonlar'
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user} -> {self.product.title}"