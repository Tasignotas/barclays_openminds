from django.db import models


class Offer(models.Model):
    ACTIONS = [('buy', 'Buy'), ('sell', 'Sell')]
    stock_label = models.CharField(max_length=50)
    action = models.CharField(max_length=10, choices=ACTIONS)
    price = models.IntegerField(help_text='In cents')
    quantity = models.IntegerField()
    user = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
