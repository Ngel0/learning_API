from django.db import models

# Create your models here.
class Cryptocurrency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=23, decimal_places=17)
    market_cap = models.DecimalField(max_digits=18, decimal_places=5)
    volume = models.DecimalField(max_digits=25, decimal_places=8)
    percent_change = models.DecimalField(max_digits=12, decimal_places=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
