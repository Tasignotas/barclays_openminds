import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect

from creative_exchange import forms
from creative_exchange.models import Offer, Trade
from creative_exchange.trading import submit_offer

@login_required
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
    return render(request, 'trading.html', dict(trade_form=form, trades=trades, offers=offers, active_page='home'))

@login_required
def get_trade_and_order(request):
    trades = Trade.objects.order_by('-timestamp')
    offers = Offer.objects.order_by('stock_label', 'action', 'timestamp')
    ans = {}
    ans['order_book_html'] = render_to_string('order_book.html', dict(offers=offers))
    ans['trade_history_html'] = render_to_string('trade_history.html', dict(trades=trades))
    return HttpResponse(json.dumps(ans))

@login_required
def trader_test(request):
    form = forms.TraderSelectForm(request.GET)
    profit_for_stock = {}
    offers = Offer.objects.filter(user=request.user).order_by('stock_label', 'action', 'timestamp')
    if form.is_valid() and form.cleaned_data['trader'] is not None:
        for sign, trades in [(1, Trade.objects.filter(buyer=form.cleaned_data['trader'])), (-1, Trade.objects.filter(seller=form.cleaned_data['trader']))]:
            for trade in trades:
                profit_for_stock[trade.stock_label] = profit_for_stock.get(trade.stock_label, 0) + sign * trade.price * trade.quantity
    data = zip(*profit_for_stock.items())
    json_data = json.dumps(data)
    return render(request, 'trader_profile.html', { 'trader_profile_form': form, 'json_data': json_data, 'offers' : offers, 'active_page': 'portfolio' })

    
@login_required
def get_trader_orders(request):
    offers = Offer.objects.filter(user=request.user).order_by('stock_label', 'action', 'timestamp')
    return HttpResponse(render_to_string('trader_orders.html', {'offers' : offers}))
    
    
@login_required
def cancel_order(request, id):
    Offer.objects.get(id=id, user=request.user).delete()
    return redirect(trader_test)
