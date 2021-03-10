from django.db import models
from django.contrib.auth.models import User
import os

class Free_Post(models.Model):
    title=models.CharField(max_length=30)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    author=models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.pk}]{self.title}by{self.author}'

    def get_free_url(self):
        return f'{self.pk}/'

class Free_Comment(models.Model):
    writer=models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    free_post=models.ForeignKey(Free_Post, on_delete=models.CASCADE)
    text=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.writer.username+'::'+self.text


