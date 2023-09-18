import requests
from .models import Cryptocurrency
from django.views.generic import ListView
import os
from django.core.paginator import Paginator


# Create your views here.
# Class for handling API from CoinMarketCap
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

# Scheduled api call
def fetch_cryptocurrency_data(limit):
    api_key = os.environ['API_KEY']
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
                'percent_change_1h': coin['quote']['USD']['percent_change_1h'],
                'percent_change_24h': coin['quote']['USD']['percent_change_24h'],
                'percent_change_7d': coin['quote']['USD']['percent_change_7d'],
            }
        )

class ListCoinsView(ListView):
    model = Cryptocurrency
    context_object_name = 'cryptocurrencies'
    paginate_by = 30

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-market_cap')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        paginator = Paginator(self.model.objects.order_by('-market_cap'), self.paginate_by)
        page_number = int(self.request.GET.get('page', 1))
        cryptocurrencies = paginator.get_page(page_number)
        context['cryptocurrencies'] = cryptocurrencies
        return context
