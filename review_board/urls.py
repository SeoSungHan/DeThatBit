from django.urls import path
from . import views

urlpatterns=[
    path('<int:pk>/',views.Review_Detail.as_view()),
    path('',views.Review_List.as_view()),
]