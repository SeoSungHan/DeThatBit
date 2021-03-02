from django.contrib import admin
from django.urls import path,include
from .import views

app_name="single_pages"

urlpatterns = [
    path('about_this/', views.about_this),
    path('', views.landing),
    path('login/', views.login),
    path('sign_up/', views.sign_up, name="sign_up"),
]