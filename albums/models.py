from django.db import models
import os
import math


class Albums(models.Model):
    artist = models.CharField(max_length=500)
    a_type = models.CharField(max_length=10)
    album = models.CharField(max_length=500)
    date = models.DateField()
    cover = models.CharField(max_length=500)
    link = models.CharField(max_length=500, null=True)

    rating = models.FloatField(default=0)
    reviews = models.IntegerField(default=0)

    def __str__(self):
        return self.artist+'::'+self.album

    def get_round_rating(self):
        return round(self.rating,2)
        