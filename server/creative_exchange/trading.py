import collections

from creative_exchange.models import Offer

Trade = collections.namedtuple('Trade', 'stock_label seller buyer price quantity')

def submit_offer(offer):
    result_trades = []
    buy = offer.action == 'buy'
    possible_trades = Offer.objects.filter(stock_label=offer.stock_label)
    if buy:
        possible_trades = (possible_trades.filter(action='sell',
                                              price__lte=offer.price)
                                              .order_by('price', 'timestamp'))
    else:
        possible_trades = (possible_trades.filter(action='buy',
                                              price__gte=offer.price)
                                              .order_by('timestamp'))
    for trade_offer in possible_trades:
        trade_quantity = min(offer.quantity, trade_offer.quantity)
        if trade_quantity > 0:
            seller, buyer = (trade_offer.user, offer.user) if buy else (offer.user, trade_offer.user)
            trade_price = min(offer.price, trade_offer.price)
            result_trades.append(Trade(offer.stock_label, seller, buyer, trade_price, trade_quantity))
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
    return result_trades
