from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Offer(models.Model):
    ACTIONS = [('buy', 'Buy'), ('sell', 'Sell')]
    stock_label = models.CharField(max_length=50)
    action = models.CharField(max_length=10, choices=ACTIONS)
    price = models.IntegerField(help_text='In cents', validators=[MinValueValidator(1)])
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)

class Trade(models.Model):
    stock_label = models.CharField(max_length=50)
    seller = models.ForeignKey(User, related_name='trades_sold')
    buyer = models.ForeignKey(User, related_name='trades_bought')
    price = models.IntegerField(help_text='In cents')
    quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
