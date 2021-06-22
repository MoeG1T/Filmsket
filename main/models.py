from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.


class Basket(models.Model):
    BasketGenre = models.CharField(max_length=200)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE, related_name="basket", null=True)

    class Meta:
        verbose_name_plural = "Baskets"

    def __str__(self):
        return self.BasketGenre

class Film(models.Model):
    name = models.CharField(max_length=200, null=True)
    date = models.DateTimeField("date created", default=datetime.now())
    done = models.BooleanField(default=False)
    
    BasketGenre = models.ForeignKey(Basket, default=1, verbose_name="basket", on_delete=models.SET_DEFAULT)
    
    def __str__(self):
        return self.name

class Result(models.Model):
    result = models.CharField(max_length=200)
    Num = models.IntegerField()