from django import forms

from creative_exchange import models

class OfferForm(forms.ModelForm):
    ORDER_TYPES = [
        ('market', 'Market Order'),
        ('limit', 'Limit Order'),
        ('day', 'Day Order (24 hours)'),
        ('ioc', 'Immediate or Cancel'),
        ('fok', 'Fill or Kill'),
    ]
    
    class Meta:
        model = models.Offer
        exclude = ('user',)
        widgets = {
            'action': forms.RadioSelect
        }
    
    order_type = forms.ChoiceField(choices=ORDER_TYPES)
    action = forms.ChoiceField(choices=models.Offer.ACTIONS, widget=forms.RadioSelect)
