from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class UserForm(UserCreationForm):
    email=models.EmailField(verbose_name="Email")

    class Meta:
        model=User
        fields=("username","email")

