from django.urls import path
from accountmanager import views

urlpatterns = [
    path("", views.accountMngrTable, name="home"),
    path("accountManagerTable", views.accountMngrTable, name="viewTable"),
    path("accountManagerStatements", views.accountMngrStatements, name="viewStatements"),
    path("accountManagerAdd", views.accountMngrAdd, name="inputData"),
    path("accountManagerAddRecieved", views.accountMngrAddRecieved, name="recievedData"),
    path("accountManagerRemove", views.accountMngrRemove, name="removeAccount"),
    path("accountManagerEdit", views.accountMngrEdit, name="editAccount"),
    path("accountManagerEditRecieved", views.accountMngrEditRecieved, name="editAccount"),
    path("accountManagerRemoveRecieved", views.accountMngrRemoveRecieved, name="editAccount"),

    path('logout-am/', views.user_logout, name='user-logout-am')
]