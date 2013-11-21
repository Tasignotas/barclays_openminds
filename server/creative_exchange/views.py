from django.shortcuts import render, redirect

from creative_exchange import forms
from creative_exchange.models import Offer
from creative_exchange.trading import submit_offer

def trading(request):
    initial = {'stock_label': 'vod.l'}
    if request.method == 'POST':
        form = forms.OfferForm(request.POST, initial=initial)
        if form.is_valid():
            obj = form.save(commit=False)
            trades = submit_offer(obj)
            request.session['trades'] = trades
            return redirect(trading)
    else:
        form = forms.OfferForm(initial=initial)
    if 'trades' in request.session:
        trades = request.session['trades']
        del request.session['trades']
    else:
        trades = []
    offers = Offer.objects.order_by('stock_label', 'action', 'timestamp')
    return render(request, 'trading.html', dict(trade_form=form, trades=trades, offers=offers))
