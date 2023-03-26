from django.shortcuts import render, redirect
from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId
import datetime
import re
import string
import random

client = pymongo.MongoClient("mongodb+srv://choo2foonyee:FpaMQ6825hCyJw6x@uweflix.l8xahep.mongodb.net/?retryWrites=true&w=majority")
# database
db = client.test
# collection 
Showings = db.Showings

def select_date(request):
    return render(request, 'cust/select_date.html')

def view_data(request):
    selected_date = request.GET.get('date')
    results = Showings.find({'date': {'$gte': selected_date}})
    context = {'results': results, 'selected_date': selected_date}
    return render(request, 'cust/data_view.html', context)
