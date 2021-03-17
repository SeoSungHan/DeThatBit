from django.db import models
from django.contrib.auth.models import User
from albums.models import Albums
import os

class Review_Post(models.Model):
    title=models.CharField(max_length=30)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    rating=models.FloatField(default=0)

    album=models.ForeignKey(Albums, null=True, on_delete=models.SET_NULL)
    author=models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'[{self.pk}]{self.title}by{self.author}'

    def get_review_url(self):
        return f'/review/{self.pk}/'
