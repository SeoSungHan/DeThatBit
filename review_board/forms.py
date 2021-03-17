from django import forms

from .models import Review_Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Review_Post
        fields = ('album','title', 'content', 'rating')

