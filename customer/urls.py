from django.urls import path
from cust import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),

    path("selectDate/", views.selectDate, name="selectDate"),
    path("selectDate/booking/<str:selectedDate>", views.booking, name="booking"),
    path("payment/<int:adultQuantity>-<int:studentQuantity>-<int:childQuantity>-<int:selectedShowing>", views.payment, name="payment"),
]