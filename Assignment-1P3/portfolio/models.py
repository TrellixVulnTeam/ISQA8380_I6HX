from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import requests
import logging


class Customer(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    cust_number = models.IntegerField(blank=False, null=False)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    email = models.EmailField(max_length=200)
    cell_phone = models.CharField(max_length=50)
    created_date = models.DateTimeField(
        default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.cust_number)


class Investment(models.Model):
    customer = models.ForeignKey(Customer, related_name='investments')
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    acquired_value = models.DecimalField(max_digits=10, decimal_places=2)
    acquired_date = models.DateField(default=timezone.now)
    recent_value = models.DecimalField(max_digits=10, decimal_places=2)
    recent_date = models.DateField(default=timezone.now, blank=True, null=True)

    def created(self):
        self.acquired_date = timezone.now()
        self.save()

    def updated(self):
        self.recent_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.customer)

    def results_by_investment(self):
        return self.recent_value - self.acquired_value


class Stock(models.Model):
    customer = models.ForeignKey(Customer, related_name='stocks')
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    shares = models.DecimalField (max_digits=10, decimal_places=1)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField(default=timezone.now, blank=True, null=True)

    def created(self):
        self.recent_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.customer)

    def initial_stock_value(self):
        return self.shares * self.purchase_price


class MutualFunds(models.Model):
    customer = models.ForeignKey(Customer, related_name='MutualFunds')
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    funds = models.DecimalField(max_digits=10, decimal_places=1)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField(default=timezone.now, blank=True, null=True)

    def created(self):
        self.recent_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.customer)

    def initial_MutualFunds_value(self):
        return self.funds * self.purchase_price


    def current_stock_price(self):
        symbol_f = str(self.symbol)
        main_api = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='
        api_key = '&interval=1min&apikey=7O7YNBY5DKGBT30V'
        url = main_api + symbol_f + api_key
        print(url)
        json_data = requests.get(url).json()
        mkt_dt = (json_data["Meta Data"]["3. Last Refreshed"])
        open_price = float(json_data["Time Series (1min)"][mkt_dt]["1. open"])
        share_value = open_price
        return share_value

    def current_stock_value(self):
        symbol_f = str(self.symbol)
        main_api = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='
        api_key = '&interval=1min&apikey=7O7YNBY5DKGBT30V'
        url = main_api + symbol_f + api_key
        print(url)
        json_data = requests.get(url).json()
        mkt_dt = (json_data["Meta Data"]["3. Last Refreshed"])
        open_price = float(json_data["Time Series (1min)"][mkt_dt]["1. open"])
        share_value = open_price
        return float(share_value) * float(self.shares)





