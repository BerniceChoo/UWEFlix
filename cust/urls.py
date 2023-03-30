from django.urls import path
from cust import views

urlpatterns = [
    path('', views.select_date, name='select_date'),
    path('view_data/', views.view_data, name='view_data'),

    path('view_data/ticket/', views.ticket, name='ticket'),
    path('view_data/ticket/book_tickets/', views.book_tickets, name='book_tickets'),

    path('view_data/ticket/book_tickets/booking_confirmation/', views.confirmation, name='confirmation'),
]