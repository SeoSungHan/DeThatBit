from django.urls import path
from . import views

urlpatterns=[
    path('',views.Albums_List.as_view()),
]