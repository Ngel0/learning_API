from .models import Favourite
from cryptodata.models import Cryptocurrency
from django.views import View
from django.views.generic import ListView
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache


class FavouriteAddOrDelete(View):
    def post(self, request):
        user = request.user
        coin_id = request.POST.get('coin_id')
        coin = Cryptocurrency.objects.get(id=coin_id)
        obj, created = Favourite.objects.get_or_create(user=user, cryptocurrency=coin)
        if not created:
            obj.delete()
        return JsonResponse({'status': 'OK'})


class FavouritesListView(LoginRequiredMixin, ListView):
    model = Cryptocurrency
    context_object_name = 'cryptocurrencies'
    paginate_by = 30
    template_name = 'favourites/watchlist.html'

    # only favourited coins get in queryset
    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.user.id
        favourites_id_cache_key = f'favourites_{user_id}'
        favourites_id = cache.get(favourites_id_cache_key)
        if not favourites_id:
            favourites_id = Favourite.objects.filter(user=user_id).values_list('cryptocurrency_id', flat=True)
            cache.set(favourites_id_cache_key, favourites_id, 60 * 5)
        return queryset.filter(id__in=favourites_id).order_by('rank')
