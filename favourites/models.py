from django.db import models
from django.contrib.auth.models import User


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cryptocurrency = models.ForeignKey('cryptodata.Cryptocurrency', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'cryptocurrency')

    def __str__(self):
        return f'{self.user.username}\'s favorite: {self.cryptocurrency.name}'
