from django.urls import path
from . import views

urlpatterns=[
    path('<int:pk>/',views.Review_Detail.as_view()),
    path('',views.Review_List.as_view()),
    path('<int:pk>/comment_create/', views.Review_Comment_Create,name="comment_create"),
    path('comment_update/<int:pk>/', views.Review_Comment_Update,name="comment_update"),
    path('comment_delete/<int:pk>/', views.Review_Comment_Delete,name="comment_delete"),
    path('create/',views.Review_Post_Create,name="review_create"),
    path('<int:pk>/update/',views.Review_Post_Update,name="review_update"),
    path('<int:pk>/delete/',views.Review_Post_Delete,name="review_delete"),
]