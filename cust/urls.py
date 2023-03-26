from django.urls import path
from cust import views

urlpatterns = [
    #path('', views.dates_list, name='dates-list'),
    #path('edit/<str:selectedDate>/', views.showings_list, name='showings-list'),
    path('', views.select_date, name='select_date'),
    path('view_data/', views.view_data, name='view_data')
    #path('select_date/', views.showings_list, name='showings-list'),
    # path('select_date/', views.select_date, name='select_date')
    #path("", views.home, name="home"),
    #path("home", views.home, name="home"),

    #path("selectDate/", views.selectDate, name="selectDate"),
    #path("selectDate/booking/<str:selectedDate>", views.booking, name="booking"),
    #path("payment/<int:adultQuantity>-<int:studentQuantity>-<int:childQuantity>-<int:selectedShowing>", views.payment, name="payment"),
]