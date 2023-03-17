from django.urls import path
from . import views

urlpatterns = [
    path('', views.clubs_list, name='clubs-list'),

]

"""
    path('create/', views.create_club, name='create-club'),
    path('edit/<str:pk>/', views.edit_club, name='edit-club'),
    path('delete/<str:pk>/', views.delete_club, name='delete-club'),
"""