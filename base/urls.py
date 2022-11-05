from django.urls import path
from . import views




urlpatterns = [
    path('login/', views.Log_in, name='login'),
    path('logout/', views.Log_out, name='logout'),
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),
    path('room/<str:id>/', views.room , name='room'),
    path('create-room/', views.create_room , name='create-room'),
    path('delete-room/<str:id>/', views.delete_room , name='delete-room'),
    path('update-room/<str:id>/', views.update_room , name='update-room'),
    path('delete-message/<str:id>/', views.delete_msg , name='delete-message'),
    path('profile/<str:id>/', views.profile , name='profile'),
    path('update-user/', views.user_update , name='update-user'),
    path('upload-file/<str:id>/', views.upload_file , name='upload-file'),
    path('room/<str:id>/files', views.room_files , name='room-files'),
    path('predict-gpa', views.predict_gpa , name='predict-gpa'),
    path('predict-category', views.predict_category , name='predict-category'),

]