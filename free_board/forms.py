from django import forms

from .models import Free_Post, Free_Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Free_Post
        fields = ('title', 'content',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Free_Comment
        fields = ('text',)
