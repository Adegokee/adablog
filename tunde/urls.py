from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('createRoom', views.createRoom, name='createRoom'),
     path('editRoom/<str:pk>/', views.editRoom, name='editRoom'),
    path('deleteRoom/<str:pk>/', views.deleteRoom, name='deleteRoom'),
    path('login/', views.loginUser, name='login'),
     path('logout/', views.logoutUser, name='logout'),
     path('register/', views.registerUser, name='register'),
      path('delete-message/<str:pk>/', views.deleteMessage, name='delete-message'),
       path('profile/<str:pk>/', views.userProfile, name='profile'),
       path('update/', views.updateUser, name='update'),
        path('topic/', views.topicPage, name='topic'),
        path('activity/', views.activityPage, name='activity'),
        
       
    
]
