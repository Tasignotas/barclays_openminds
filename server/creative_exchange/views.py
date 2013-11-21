from django.shortcuts import render, redirect

from creative_exchange import forms
from creative_exchange.models import Offer, Trade
from creative_exchange.trading import submit_offer

def trading(request):
    initial = {'stock_label': 'vod.l'}
    if request.method == 'POST':
        form = forms.OfferForm(request.POST, initial=initial)
        if form.is_valid():
            obj = form.save(commit=False)
            trades = submit_offer(obj)
            for trade in trades:
                Trade.objects.create(stock_label=trade.stock_label,
                                     seller=trade.seller,
                                     buyer=trade.buyer,
                                     price=trade.price,
                                     quantity=trade.quantity)
            current_trades = request.session['trades']
            request.session['trades'] = current_trades + trades
            return redirect(trading)
    else:
        form = forms.OfferForm(initial=initial)
    if 'trades' in request.session:
        trades = request.session['trades']
    else:
        trades = []
    offers = Offer.objects.order_by('stock_label', 'action', 'timestamp')
    return render(request, 'trading.html', dict(trade_form=form, trades=trades, offers=offers))
