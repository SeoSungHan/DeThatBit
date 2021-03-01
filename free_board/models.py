from django.db import models
import os

class Free_Post(models.Model):
    title=models.CharField(max_length=30)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.pk}]{self.title}'

    def get_free_url(self):
        return f'{self.pk}/'
