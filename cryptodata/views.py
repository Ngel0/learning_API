import requests
import os

from django.views.generic import ListView
from django.core.paginator import Paginator
from django.core.cache import cache

from favourites.models import Favourite
from .models import Cryptocurrency


# Class for handling API from CoinMarketCap
# https://coinmarketcap.com/api/documentation/v1/
class CoinMarketCap:
    # initializing base url and headers for all api calls
    def __init__(self, token) -> None:
        self.api_url = 'https://pro-api.coinmarketcap.com'
        self.headers = {'Accept': 'application/json',
                        'Accept - Encoding': 'deflate, gzip',
                        'X-CMC_PRO_API_KEY': token, }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    # unique CoinMarketCap ID mapping
    def get_all_coins_mapping(self):
        url = self.api_url + '/v1/cryptocurrency/map'
        parameters = {'limit': '10'}
        response = self.session.get(url, params=parameters)
        if response.status_code == 200:
            return response.json()['data']
        else:
            response.raise_for_status()

    # latest market data for limit number of coins
    def get_latest_data(self, limit=100):
        url = self.api_url + '/v1/cryptocurrency/listings/latest'
        parameters = {'limit': limit}
        response = self.session.get(url, params=parameters)
        if response.status_code == 200:
            return response.json()['data']
        else:
            response.raise_for_status()


# function fetches and saves limit number of coin data for Scheduled api calls
def fetch_cryptocurrency_data(limit):
    api_key = os.getenv('API_KEY')
    cryptocurrencies = CoinMarketCap(api_key).get_latest_data(limit)
    for coin in cryptocurrencies:
        Cryptocurrency.objects.update_or_create(
            id=coin['id'],
            defaults={
                'rank': coin['cmc_rank'],
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


# ListView for displaying all coins
class CoinsListView(ListView):
    model = Cryptocurrency
    context_object_name = 'cryptocurrencies'
    paginate_by = 30

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('rank')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user_id = self.request.user.id
        favourites_id_cache_key = f'favourites_{user_id}'
        favourites_id = cache.get(favourites_id_cache_key)
        if not favourites_id:
            favourites_id = Favourite.objects.filter(user=user_id).values_list('cryptocurrency_id', flat=True)
            cache.set(favourites_id_cache_key, favourites_id, 60 * 5)
        context['favourites'] = favourites_id
        return context
