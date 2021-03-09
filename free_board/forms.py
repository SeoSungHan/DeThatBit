from django import forms

from .models import Free_Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Free_Post
        fields = ('title', 'content',)