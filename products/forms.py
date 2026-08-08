from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'category', 'condition', 'price', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E\'lon sarlavhasini kiriting'}),
            'category': forms.Select(attrs={'class': 'form-select', 'id': 'categorySelect'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: 1500000'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Mahsulot haqida batafsil ma\'lumot...'}),
        }

    # 1. 🚗 AVTOMOBIL
    auto_year = forms.IntegerField(required=False, label="Yili", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2022'}))
    auto_mileage = forms.IntegerField(required=False, label="Bosgan masofasi (km)", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '50000'}))
    auto_fuel = forms.CharField(required=False, label="Yoqilg'i turi", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Benzin, Gaz, Elektrmobil'}))
    auto_transmission = forms.CharField(required=False, label="Uzatmalar qutisi", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Avtomat / Mexanika'}))

    # 2. 📱 TEXNIKA / TELEFON
    tech_brand = forms.CharField(required=False, label="Brend", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apple, Samsung'}))
    tech_memory = forms.CharField(required=False, label="Xotirasi", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '128 GB'}))
    tech_color = forms.CharField(required=False, label="Rangi", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Qora, Oltin'}))

    # 3. 🏠 KO'CHMAS MULK
    home_rooms = forms.IntegerField(required=False, label="Xonalar soni", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '3'}))
    home_area = forms.FloatField(required=False, label="Maydoni (m²)", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '75'}))
    home_floor = forms.IntegerField(required=False, label="Qavati", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '4'}))

    # 4. 🍏 OZIQ-OVQAT
    food_weight = forms.CharField(required=False, label="O'lchami / Og'irligi", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10 kg'}))
    food_expiry = forms.CharField(required=False, label="Yaroqlilik muddati", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12 oy'}))

    # 5. 👕 KIYIM VA POYABZAL
    clothing_size = forms.CharField(required=False, label="O'lchami (Size)", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'M, L, XL, 42'}))
    clothing_gender = forms.CharField(required=False, label="Kim uchun", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Erkaklar / Ayollar / Bolalar'}))

    # 6. 🛋️ MEBEL
    furniture_material = forms.CharField(required=False, label="Materiali", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Yog\'och, Mdf, Charm'}))

    # 7. 🛠️ XIZMATLAR
    service_type = forms.CharField(required=False, label="Xizmat turi", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ta\'mirlash, Yetkazib berish'}))

    # 8. 🐶 UY HAYVONLARI
    pet_age = forms.CharField(required=False, label="Yoshi / Zoti", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1 yosh, Xaski'}))

    # 9. 💼 ISH O'RINLARI
    job_salary = forms.CharField(required=False, label="Maosh", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '5 000 000 so\'m'}))
    job_type = forms.CharField(required=False, label="Bandlik turi", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'To\'liq kun / Masofaviy'}))

    # 10. ⚽ SPORT VA XOBBI
    sport_category = forms.CharField(required=False, label="Sport turi", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Futbol, Fitness'}))

    # 11. 📚 KITOBLAR VA KANTSOVAR
    book_author = forms.CharField(required=False, label="Muallif", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'O\'tkir Hoshimov'}))
    book_genre = forms.CharField(required=False, label="Janri / Turi", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Badiiy'}))