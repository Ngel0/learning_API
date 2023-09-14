from django.shortcuts import render
import requests
from .models import Cryptocurrency
from django.http import HttpResponse
from django.views.generic import ListView
import os

# Create your views here.
class CoinMarketCap:
    #https://coinmarketcap.com/api/documentation/v1/
    def __init__(self, token) -> None:
        self.api_url = 'https://pro-api.coinmarketcap.com'
        self.headers = {'Accepts': 'application/json',
                        'X-CMC_PRO_API_KEY': token, }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_all_coins(self):#definitely need to change sth
        url = self.api_url + '/v1/cryptocurrency/map'
        parameters = {'limit': '10'}
        response = self.session.get(url, params=parameters)
        if response.status_code == 200:
            data = response.json()['data']#else raise error ?
        return data

    def get_latest_data(self, limit=100):
        url = self.api_url + '/v1/cryptocurrency/listings/latest'
        parameters = {'limit': limit}
        response = self.session.get(url, params=parameters)
        if response.status_code == 200:
            data = response.json()['data']
        return data

    def get_price_symbol(self, symbol):
        url = self.api_url + '/v2/cryptocurrency/quotes/latest'
        parameters = {'symbol': symbol}
        response = self.session.get(url, params=parameters)
        if response.status_code == 200:
            data = response.json()['data']
        return data

def fetch_cryptocurrency_data():
    api_key = os.environ['API_KEY']
    limit = 150
    cryptocurrencies = CoinMarketCap(api_key).get_latest_data(limit)
    for coin in cryptocurrencies:
        Cryptocurrency.objects.update_or_create(
            symbol=coin['symbol'],
            defaults={
                'name': coin['name'],
                'symbol': coin['symbol'],
                'price': coin['quote']['USD']['price'],
                'market_cap': coin['quote']['USD']['market_cap'],
                'volume': coin['quote']['USD']['volume_24h'],
                'percent_change': coin['quote']['USD']['percent_change_24h'],
            }
        )

class ListCoinsView(ListView):
    model = Cryptocurrency
    #template_name = 'cryptocurrency_list.html'
    context_object_name = 'cryptocurrencies'
