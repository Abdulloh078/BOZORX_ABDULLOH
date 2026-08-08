from django import forms
from .models import Product, Review


class ProductForm(forms.ModelForm):
    # -------------------------------------------------------------
    # DINAMIK KATEGORIYALAR UCHUN QO'SHIMCHA MAYDONLAR
    # -------------------------------------------------------------

    # 1. 🚗 AVTOMOBILLAR VA EHTIYOT QISMLAR
    auto_year = forms.IntegerField(
        required=False,
        label="Chiqarilgan yili",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: 2022'})
    )
    auto_mileage = forms.IntegerField(
        required=False,
        label="Yurgan masofasi (km)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: 85000'})
    )
    auto_fuel = forms.ChoiceField(
        required=False,
        label="Yoqilg'i turi",
        choices=[
            ('', '-- Tanlang --'),
            ('benzin', 'Benzin'),
            ('gaz', 'Gaz (Metan/Propan)'),
            ('dizel', 'Dizel'),
            ('elektr', 'Elektrokar'),
            ('gibrid', 'Gibrid'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    auto_transmission = forms.ChoiceField(
        required=False,
        label="Uzatmalar qutisi (Korobka)",
        choices=[
            ('', '-- Tanlang --'),
            ('avtomat', 'Avtomat'),
            ('mexanika', 'Mexanika'),
            ('variator', 'Variator'),
            ('robot', 'Robot'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # 2. 📱 TELEFON VA ELEKTRONIKA
    tech_brand = forms.CharField(
        required=False,
        label="Brendi / Markasi",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: Apple, Samsung, Xiaomi'})
    )
    tech_memory = forms.CharField(
        required=False,
        label="Xotirasi (RAM / ROM)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: 8GB / 256GB'})
    )
    tech_color = forms.CharField(
        required=False,
        label="Rangi",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: Qora, Oltin, Kumushrang'})
    )

    # 3. 🏠 KO'CHMAS MULK (UY / PATIR / YER)
    home_rooms = forms.IntegerField(
        required=False,
        label="Xonalar soni",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: 3'})
    )
    home_area = forms.CharField(
        required=False,
        label="Maydoni (m²)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: 75 m² yoki 6 sotix'})
    )
    home_floor = forms.CharField(
        required=False,
        label="Qavati (Joylashgan / Jami qavat)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: 4/9'})
    )

    # 4. 🍏 OZIQ-OVQAT VA QISHLOQ XO'JALIGI
    food_weight = forms.CharField(
        required=False,
        label="Hajmi / Og'irligi / Miqdori",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: 50 kg, 2 tonna, 10 litr'})
    )
    food_expiry = forms.CharField(
        required=False,
        label="Yaroqlilik / Saqlash muddati",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: 6 oy, 12 oy'})
    )

    # 5. 👕 KIYIM VA POYABZAL
    clothing_size = forms.CharField(
        required=False,
        label="O'lchami (Size / Razmer)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: M, XL, 42, 43'})
    )
    clothing_gender = forms.ChoiceField(
        required=False,
        label="Kim uchun mo'ljallangan",
        choices=[
            ('', '-- Tanlang --'),
            ('erkak', 'Erkaklar uchun'),
            ('ayol', 'Ayollar uchun'),
            ('bolalar', 'Bolalar uchun'),
            ('unisex', 'Unisex'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # 6. 🛋️ MEBEL VA UY JIXOZLARI
    furniture_material = forms.CharField(
        required=False,
        label="Materiali / Turi",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: Yog\'och, MFD, Charm, Laminat'})
    )

    # 7. 🛠️ XIZMATLAR
    service_type = forms.CharField(
        required=False,
        label="Xizmat turi / Yo'nalishi",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: Uy ta\'mirlash, Yuk tashish, Santexnika'})
    )

    # 8. 🐶 UY HAYVONLARI
    pet_age = forms.CharField(
        required=False,
        label="Yoshi / Zoti (Poroda)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: 6 oylik, Nemis ovcharkasi'})
    )

    # 9. 💼 ISH O'RINLARI VA VAKANSIYALAR
    job_salary = forms.CharField(
        required=False,
        label="Oylik maosh / Ish haqi",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: 5 000 000 so\'m / kelishiladi'})
    )
    job_type = forms.ChoiceField(
        required=False,
        label="Ish grafigi / Bosh bandlik",
        choices=[
            ('', '-- Tanlang --'),
            ('full', 'To\'liq kun (Full-time)'),
            ('part', 'Yarim kun (Part-time)'),
            ('remote', 'Masofaviy (Online)'),
            ('freelance', 'Smena / Bir martalik'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # 10. ⚽ SPORT VA XOBBI
    sport_category = forms.CharField(
        required=False,
        label="Sport yoki xobbi turi",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: Velosport, Trenajyor, Musiqa asboblari'})
    )

    # -------------------------------------------------------------
    # ASOSIY MODEL MAYDONLARI
    # -------------------------------------------------------------
    class Meta:
        model = Product
        fields = ['title', 'category', 'price', 'description', 'condition']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'E\'lon sarlavhasini kiriting'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
                'id': 'categorySelect'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Narxi (so\'mda)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Mahsulot haqida batafsil ma\'lumot...'
            }),
            'condition': forms.Select(attrs={
                'class': 'form-select'
            }),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f"{i} ⭐") for i in range(1, 6)],
                attrs={'class': 'form-select'}
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Mahsulot yoki sotuvchi haqida fikringizni qoldiring...'
                }
            ),
        }