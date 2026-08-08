from django.core.management.base import BaseCommand
from products.models import Category

class Command(BaseCommand):
    help = "Baza uchun boshlang'ich kategoriyalarni qo'shadi"

    def handle(self, *args, **kwargs):
        categories = [
            "Elektronika va Texnika",
            "Kiyim-kechak",
            "Aksessuarlar",
            "Uy va Bog'",
            "Avtomobillar",
            "Bolalar dunyosi"
        ]

        for cat_name in categories:
            category, created = Category.objects.get_or_create(name=cat_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Qo'shildi: {cat_name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Allaqachon mavjud: {cat_name}"))