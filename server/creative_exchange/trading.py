from creative_exchange.models import Offer


def submit_offer(offer):
    buy = offer.action == 'buy'
    if buy:
        possible_trades = (Offer.objects.filter(action='sell',
                                              stock_label=offer.stock_label,
                                              price__lte=offer.price)
                                              .order_by('price', 'timestamp'))
    else:
        possible_trades = (Offer.objects.filter(action='buy',
                                              stock_label=offer.stock_label,
                                              price__gte=offer.price)
                                              .order_by('timestamp'))
    for trade_offer in possible_trades:
        trade_quantity = min(offer.quantity, trade_offer.quantity)
        if trade_quantity > 0:
            if buy:
                announce_trade(offer.stock_label, trade_offer.user,
                            offer.user, trade_offer.price, trade_quantity)
            else:
                announce_trade(offer.stock_label, offer.user,
                            trade_offer.user, offer.price, trade_quantity)
        trade_offer.quantity -= trade_quantity
        if trade_offer.quantity == 0:
            trade_offer.delete()
        else:
            trade_offer.save()
        
        offer.quantity -= trade_quantity
        if offer.quantity == 0:
            break
    if offer.quantity > 0:
        offer.save()


def announce_trade(stock_label, selling_user, buying_user, price, quantity):
    print 'TRADE', stock_label, selling_user, '->', buying_user, '$', price, 'x', quantity
