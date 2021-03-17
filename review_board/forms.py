from django import forms

from .models import Review_Post, Review_Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Review_Post
        fields = ('album','title', 'content', 'rating')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Review_Comment
        fields = ('text',)


