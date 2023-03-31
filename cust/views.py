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
TicketsPrice = db.TicketsPrice

def select_date(request):
    return render(request, 'cust/select_date.html')

def view_data(request):
    selected_date = request.GET.get('date')
    results = Showings.find({'date': selected_date})
    movies = Showings.find({'date': selected_date}, {'filmTitle': 1})
    context = {'results': results, 'selected_date': selected_date, 'movies': movies}
    return render(request, 'cust/data_view.html', context)


def confirmation(request):
    number = random.randint(1, 10000000)
    return render(request, 'cust/confirmation.html', {'number': number})

def ticket(request):
    selected_data = request.GET.get('data')
    results = Showings.find({'filmTitle': selected_data})
    context = {'results': results, 'selected_data': selected_data}
    return render(request, 'cust/ticket.html', context)

def book_tickets(request):
    selected_ticketsnum = request.GET.get('tickets')
    ticket_price = TicketsPrice.find_one()['customerPrice']
    total_price = int(selected_ticketsnum) * ticket_price
    context = { 'selected_ticketsnum': selected_ticketsnum, 'ticket_price': ticket_price, 'total_price': total_price}
    return render(request, 'cust/book_tickets.html', context)