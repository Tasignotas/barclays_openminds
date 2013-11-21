from django import forms

from creative_exchange import models

class OfferForm(forms.ModelForm):
    class Meta:
        model = models.Offer
