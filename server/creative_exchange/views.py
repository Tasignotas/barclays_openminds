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
    
def offer_json(request):
    answer = '<tr><th>Stock Label</th><th>Action</th><th>Price</th><th>Quantity</th><th>User</th><th>Timestamp</th></tr>'
    offers = Offer.objects.order_by('stock_label', 'action', 'timestamp')
    if len(offers) == 0:
        return HttpResponse(answer + '<tr><td colspan="6" align="center">No offers available</td></tr>')
    for offer in offers:
        answer += '<tr><td>' + offer.stock_label + '</td><td>' + offer.get_action_display() + '</td><td>' + str(offer.price) + '</td><td>' + str(offer.quantity) + '</td><td>' + offer.user + '</td><td>' + offer.timestamp + '</td></tr>'
    return HttpResponse(answer)

def trader_test(request):
    form = forms.TraderSelectForm(request.GET)
    profit_for_stock = {}
    if form.is_valid() and form.cleaned_data['trader'] is not None:
        trades_as_buyer = Trade.objects.filter(buyer=form.cleaned_data['trader'])
        for buy in trades_as_buyer:
            if buy.stock_label in profit_for_stock:
                profit_for_stock[buy.stock_label] += buy.price * buy.quantity
            else:
                profit_for_stock[buy.stock_label] = buy.price * buy.quantity
        trades_as_seller = Trade.objects.filter(seller=form.cleaned_data['trader'])
        for sell in trades_as_seller:
            if buy.stock_label in profit_for_stock:
                profit_for_stock[sell.stock_label] -= sell.price * sell.quantity
            else:
                profit_for_stock[sell.stock_label] = - sell.price * sell.quantity
    return render(request, 'trader_profile.html', { 'trader_profile_form': form, 'profit_for_stock': profit_for_stock })