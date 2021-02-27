from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [
    path('about_this/', views.about_this),
    path('', views.landing),
]