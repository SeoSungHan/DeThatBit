from django.urls import path
from . import views

urlpatterns=[
    path('search/<int:type>/<str:q>/', views.Albums_Search.as_view()),
    path('',views.Albums_List.as_view()),
]