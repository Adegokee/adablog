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
    
]
