from django.shortcuts import render, redirect
from pymongo import MongoClient
import pymongo
import datetime

client = pymongo.MongoClient("mongodb+srv://daniel2fernandes:skelJ6UzCVlG36Ei@uweflix.l8xahep.mongodb.net/?retryWrites=true&w=majority")
# database
db = client.test
# collection 
todos = db.todos


def home(request):
    return render(request, 'home/list.html')


def cinema_manager(request):
    return render(request, 'home/list.html')

def customer(request):
    return render(request, 'home/list.html')