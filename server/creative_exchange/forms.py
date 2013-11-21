from django import forms
from django.contrib.auth.models import User

from creative_exchange import models

class OfferForm(forms.ModelForm):
    class Meta:
        model = models.Offer
        exclude = ('user',)

class TraderSelectForm(forms.Form):
    trader = forms.ModelChoiceField(User.objects.filter(is_staff=False), required=False)