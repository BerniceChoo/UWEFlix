from django.urls import path
from . import views

urlpatterns = [
    path('', views.clubs_list, name='clubs-list'),
    path('create/', views.create_club, name='create-club'),
    path('edit/<str:pk>/', views.edit_club, name='edit-club'),
    path('delete/<str:pk>/', views.delete_club, name='delete-club'),

    path('register-club-rep/<str:pk>/', views.register_club_rep, name='register-club-rep'),
    path('delete-club-rep/<str:pk>/', views.delete_club_rep, name='delete-club-rep'),


    path('screen/', views.screens_list, name='screens-list'),
    path('screen/create/', views.create_screen, name='create-screen'),
    path('screen/edit/<str:pk>/', views.edit_screen, name='edit-screen'),
    path('screen/delete/<str:pk>/', views.delete_screen, name='delete-screen'),

    

]
