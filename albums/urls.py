from django.urls import path
from . import views

urlpatterns=[
    path('search/<str:q>/', views.Albums_Search.as_view()),
    path('',views.Albums_List.as_view()),
]