from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path("login/", views.login, name="login"),
    path('<str:message>/?', views.login, name='login-error'),
    path('logout/', views.user_logout, name='user-logout')

]

