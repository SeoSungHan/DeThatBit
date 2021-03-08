from django.urls import path
from . import views

urlpatterns=[
    path('<int:pk>/',views.Free_Detail.as_view()),
    path('',views.Free_List.as_view()),
    path('create/',views.Free_Post_Create,name="free_create"),
    path('<int:pk>/update/',views.Free_Post_Update,name="free_update"),
    path('<int:pk>/delete/',views.Free_Post_Delete,name="free_delete"),
]