import json
import calendar

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
import datetime

from creative_exchange import forms
from creative_exchange.models import Offer, Trade
from creative_exchange.trading import submit_offer

@login_required
def trading(request):
    initial = {}
    if request.method == 'POST':
        form = forms.OfferForm(request.POST, initial=initial)
        action = request.POST.get('action')
        if form.is_valid() and action in ['Buy', 'Sell']:
            obj = form.save(commit=False)
            obj.action = 'buy' if action == 'Buy' else 'sell'
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
    offers = Offer.objects.filter(user=request.user).order_by('stock_label', 'action', 'timestamp')
    overall = 0
    json_data = {}
    json_data['times'] = [datetime.datetime.now() - datetime.timedelta(days=2)]
    json_data['profit'] = [overall]
    for trade in Trade.objects.order_by('timestamp'):
        if trade.buyer == request.user:
            overall -= trade.quantity * trade.price
        else:
            overall += trade.quantity * trade.price
        json_data['times'].append(trade.timestamp)
        json_data['profit'].append(overall)
    json_data['times'] = [1000 * calendar.timegm(x.utctimetuple()) for x in json_data['times']]
    json_data = zip(json_data['times'], json_data['profit'])
    print json_data
    return render(request, 'trader_profile.html', { 'json_data': json.dumps(json_data), 'offers' : offers, 'active_page': 'portfolio' })

    
@login_required
def get_trader_orders(request):
    offers = Offer.objects.filter(user=request.user).order_by('stock_label', 'action', 'timestamp')
    return HttpResponse(render_to_string('trader_orders.html', {'offers' : offers}))
    
    
@login_required
def cancel_order(request, id):
    Offer.objects.get(id=id, user=request.user).delete()
    return redirect(trader_test)
