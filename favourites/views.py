from django.shortcuts import render, redirect, get_object_or_404
from .models import Favourite
from cryptodata.models import Cryptocurrency
from django.views import View
from django.views.generic import ListView
from django.http import JsonResponse
from django.core.paginator import Paginator


class FavouritesListView(ListView):
    model = Cryptocurrency
    context_object_name = 'cryptocurrencies'
    paginate_by = 30
    template_name = 'favourites/watchlist.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.user.id
        favourites_id = Favourite.objects.filter(user=user_id).values('cryptocurrency')
        return queryset.filter(id__in=favourites_id)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = int(self.request.GET.get('page', 1))
        cryptocurrencies = paginator.get_page(page_number)
        context['cryptocurrencies'] = cryptocurrencies
        return context
