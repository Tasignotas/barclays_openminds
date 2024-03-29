from django.contrib import admin

from creative_exchange import models

class OfferAdmin(admin.ModelAdmin):
    list_display = ['stock_label', 'action', 'price', 'quantity', 'user', 'timestamp']

admin.site.register(models.Offer, OfferAdmin)

class TradeAdmin(admin.ModelAdmin):
    list_display = ['stock_label', 'seller', 'buyer', 'price', 'quantity', 'timestamp']

admin.site.register(models.Trade, TradeAdmin)