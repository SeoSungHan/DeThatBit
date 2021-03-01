from django.urls import path
from . import views

urlpatterns=[
    path('<int:pk>/',views.Free_Detail.as_view()),
    path('',views.Free_List.as_view()),
]