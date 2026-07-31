from django import forms
from .models import Product, Review


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title', 
            'category', 
            'description', 
            'price', 
            'is_negotiable', 
            'condition', 
            'region', 
            'city', 
            'phone_number'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Masalan: iPhone 13 Pro Max 128GB'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 5, 
                'placeholder': "Mahsulot haqida batafsil ma'lumot..."
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Narxni kiriting'
            }),
            'is_negotiable': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'condition': forms.Select(attrs={
                'class': 'form-select'
            }),
            'region': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Masalan: Toshkent sh.'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Masalan: Chilonzor tumani'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '+998 90 123 45 67'
            }),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f"{i} ★") for i in range(5, 0, -1)], 
                attrs={'class': 'form-select'}
            ),
            'comment': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Mahsulot haqida fikringizni qoldiring...'
            }),
        }