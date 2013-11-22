from django import forms
from django.contrib.auth.models import User

from creative_exchange import models

class OfferForm(forms.ModelForm):
    ORDER_TYPES = [
        ('limit', 'Limit Order'),
        ('market', 'Market Order'),
        ('day', 'Day Order (24 hours)'),
        ('ioc', 'Immediate or Cancel'),
        ('fok', 'Fill or Kill'),
    ]
    
    class Meta:
        model = models.Offer
        exclude = ('user', 'action')
        widgets = {
            'stock_label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Stock label'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
        }
    
    order_type = forms.ChoiceField(choices=ORDER_TYPES, widget=forms.Select(attrs={'class': 'form-control'}))
