from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
import os


class Free_Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    likes = models.ManyToManyField(
        User,
        blank=True,
        related_name='free_likes'
    )

    def __str__(self):
        return f'[{self.pk}]{self.title}by{self.author}'

    def get_free_url(self):
        return f'/free/{self.pk}/'

    def get_content_markdown(self):
        return self.content

    def get_likes_num(self):
        return self.likes.count()


class Free_Comment(models.Model):
    writer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    free_post = models.ForeignKey(Free_Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.writer.username+'::'+self.text

    def get_absolute_url(self):
        return f'{self.free_post.get_free_url()}#comment-{self.pk}'
