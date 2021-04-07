from django import forms

from .models import Review_Post, Review_Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Review_Post
        fields = ('title', 'content')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Review_Comment
        fields = ('text',)
