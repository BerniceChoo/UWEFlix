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


    path('film/', views.films_list, name='films-list'),
    path('film/create/', views.create_film, name='create-film'),
    path('film/edit/<str:pk>/', views.edit_film, name='edit-film'),
    path('film/delete/<str:pk>/', views.delete_film, name='delete-film'),

    path('showing/', views.showing_list, name='showing-list'),
    path('showing/select/', views.select_showing, name='select-showing'),
    path('showing/select/<str:pk>/', views.add_showing, name='add-showing'),
    path('showing/edit/<str:pk>/', views.edit_showing, name='edit-showing'),
    path('showing/delete/<str:pk>/', views.delete_showing, name='delete-showing'),
    

    path('logout-cm/', views.user_logout, name='user-logout-cm')

    

]
