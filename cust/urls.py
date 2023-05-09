from django.urls import path
from cust import views

app_name='cust'
urlpatterns = [
    path('', views.login, name='login') ,
    path('select_date/', views.select_date, name='selectdate'),
    path('view_data/', views.view_data, name='view_data'),

    path('view_data/ticket/<str:pk>/', views.ticket, name='ticket'),
    path('view_data/ticket/book_tickets/', views.book_tickets, name='book_tickets'),
    path('view_data/ticket/book_tickets/payment/', views.payment, name='payment'),
    path('view_data/ticket/book_tickets/booking_confirmation/', views.confirmation, name='confirmation'),

    path('films_list', views.films_list, name='films_list') ,
]