from django.urls import path
from . import views

urlpatterns=[
    path('<int:pk>/',views.Free_Detail.as_view()),
    path('',views.Free_List.as_view()),
    path('<int:pk>/comment_create/', views.Free_Comment_Create,name="comment_create"),
    path('comment_update/<int:pk>/', views.Free_Comment_Update,name="comment_update"),
    path('comment_delete/<int:pk>/', views.Free_Comment_Delete,name="comment_delete"),
    path('create/',views.Free_Post_Create,name="free_create"),
    path('<int:pk>/update/',views.Free_Post_Update,name="free_update"),
    path('<int:pk>/delete/',views.Free_Post_Delete,name="free_delete"),
    path('like/',views.Free_Post_Like, name="free_post_like"),
    path('search/<int:type>/<str:q>/',views.Free_Search.as_view()),
]