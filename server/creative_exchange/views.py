import json

from django.http import HttpResponse
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
            obj.user = request.user
            trades = submit_offer(obj)
            for trade in trades:
                Trade.objects.create(stock_label=trade.stock_label,
                                     seller=trade.seller,
                                     buyer=trade.buyer,
                                     price=trade.price,
                                     quantity=trade.quantity)
            return redirect(trading)
    else:
        form = forms.OfferForm(initial=initial)
    offers = Offer.objects.order_by('stock_label', 'action', 'timestamp')
    trades = Trade.objects.order_by('-timestamp')
    return render(request, 'trading.html', dict(trade_form=form, trades=trades, offers=offers))
    
def order_book(request):
    offers = Offer.objects.order_by('stock_label', 'action', 'timestamp')
    return render(request, 'order_book.html', dict(offers=offers))
