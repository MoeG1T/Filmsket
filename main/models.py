from django.db import models
from datetime import datetime
# Create your models here.


class Basket(models.Model):
    BasketGenre = models.CharField(max_length=200)
    BasketSlug = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Baskets"

    def __str__(self):
        return self.BasketGenre

class Film(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField("date created", default=datetime.now())
    done = models.BooleanField(default=False)
    
    BasketGenre = models.ForeignKey(Basket, default=1, verbose_name="basket", on_delete=models.SET_DEFAULT)
    film_slug = models.CharField(max_length=200, default=1)
    
    def __str__(self):
        return self.name
