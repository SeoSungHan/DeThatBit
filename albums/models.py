from django.db import models
import os

class Albums(models.Model):
    artist=models.CharField(max_length=30)
    a_type=models.CharField(max_length=10)
    album=models.CharField(max_length=100)
    date=models.DateField()
    cover=models.CharField(max_length=500)
    link=models.CharField(max_length=500, null = True)

    rating=models.FloatField(default=0)
    review_cnt=models.IntegerField(default=0)

    def __str__(self):
        return self.artist+'::'+self.album