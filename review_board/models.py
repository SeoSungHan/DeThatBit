from django.db import models
from django.contrib.auth.models import User
from albums.models import Albums
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
import os


class Review_Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.FloatField(default=0)

    album = models.ForeignKey(Albums, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    likes = models.ManyToManyField(
        User, blank=True, related_name='review_likes')

    def __str__(self):
        return f'[{self.pk}]{self.title}by{self.author}'

    def get_review_url(self):
        return f'/review/{self.pk}/'

    def get_content_markdown(self):
        return markdown(self.content)

    def get_likes_num(self):
        return self.likes.count()


class Review_Comment(models.Model):
    writer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    review_post = models.ForeignKey(Review_Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.writer.username+'::'+self.text

    def get_absolute_url(self):
        return f'{self.review_post.get_review_url()}#comment-{self.pk}'
