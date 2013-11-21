from django.shortcuts import render, redirect

from creative_exchange import forms
from creative_exchange.trading import submit_offer

def trading(request):
    if request.method == 'POST':
        form = forms.OfferForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            submit_offer(obj)
            return redirect(trading)
    else:
        form = forms.OfferForm()
    return render(request, 'trading.html', dict(trade_form=form))
