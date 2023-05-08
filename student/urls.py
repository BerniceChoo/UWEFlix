from django.urls import path
from . import views

urlpatterns = [
    #path('', views.login, name='login') ,
    #path('', views.login, name='logout') ,

    #path('create/', views.create_club, name='create-club'),
    #path('edit/<str:pk>/', views.edit_club, name='edit-club'),
    #path('delete/<str:pk>/', views.delete_club, name='delete-club'),

    #path('register-club-rep/<str:pk>/', views.register_club_rep, name='register-club-rep'),
    #path('delete-club-rep/<str:pk>/', views.delete_club_rep, name='delete-club-rep'),
    path('selectdate/', views.select_date, name='select-date-st'),

    path('transactions', views.view_transactions, name='view-all-transactions-st'),
    path('transactions/<str:selected_month>/?', views.view_transactions, name='view-month-transactions-st'),
    path('showing/<str:selected_date>/', views.showings_list, name='showings_list-st'),
    path('view/<str:pk>/', views.view_film, name='view-film-st'),
    path('booking/<str:pk>/<str:numb_of_tickets>', views.view_booking, name='view-booking-st'),

    path('view/<str:pk>/<str:message>/?', views.view_film, name='view-film-error-st'),

    path('logout/', views.user_logout, name='user-logout-st'),
    
    path('payment/', views.payment, name='payment-st'),

    #path('<str:message>/?', views.login, name='login-error') ,

    

]
