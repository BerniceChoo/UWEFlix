from django.shortcuts import render, redirect
from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId
import datetime
import re
import string
import random
import ssl
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from django.urls import reverse

client = "mongodb+srv://choo2foonyee:FpaMQ6825hCyJw6x@uweflix.l8xahep.mongodb.net/?retryWrites=true&w=majority"
# client = pymongo.MongoClient("mongodb+srv://choo2foonyee:FpaMQ6825hCyJw6x@uweflix.l8xahep.mongodb.net/?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
client = MongoClient(client)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("\n DATABASE NOT CONNECTED :",e)
# database
db = client.test
# collection 
Showings = db.Showings
TicketsPrice = db.TicketsPrice
Accounts = db.Accounts
Films = db.Films
print("\n Student :", Accounts)

def select_date(request):
    return render(request, 'cust/select_date.html')


def login(request, message=None):

    if request.method == 'POST':
        number = request.POST.get('number')
        print("\n Number :",number)
        password = request.POST.get('password')
        print("\n Password :",password)
        number= int(number)
        # print("\n Find One :", Student.find_one({"number": number, "password": password}))

        result = Accounts.find_one({"id": number, "Password": password})
        print("\n Result if user exists :", result)


        if result:
            print(f"Document found.")

            request.session['loggedin'] = True
            request.session['UserID'] = str(result['_id'])
            request.session['Name'] = str(result['FirstName']) + " " + str(result['LastName'])

            return redirect(reverse('cust:selectdate'))
        else:
            # Document not found
            print(f"No document found with _id.")
            message = "Your login credentials were not found. Please try again."
            return redirect('cust:login')


    context = {
        'search_query': 1,
        'data': 1,
        'message': message,
    }
    return render(request, 'cust/login.html', context)

def view_data(request):
    selected_date = request.GET.get('date')
    results = Showings.find({'date': selected_date})
    movies = Showings.find({'date': selected_date}, {'filmTitle': 1})
    data = [doc for doc in results]
    context = {'results': results, 'selected_date': selected_date, 'movies': movies, 'data': data}
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
    ticket_price = TicketsPrice.find_one()['Price']
    total_price = int(selected_ticketsnum) * ticket_price
    context = { 'selected_ticketsnum': selected_ticketsnum, 'ticket_price': ticket_price, 'total_price': total_price}
    return render(request, 'cust/book_tickets.html', context)

def films_list(request):
    
    search_query = ""
    

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
       
        
    #cursor = Clubs.find({})
    # case insensitive search using regex
    regex = re.compile(search_query, re.IGNORECASE)
    query = {'Name': {'$regex': regex}}
    cursor = Films.find(query)

    #joins showings and films collection, soo that we can see if a film is out for a showing, if it is the film cant be deleted
    pipeline = [
        {
            '$lookup': {
                'from': 'Showings',
                'localField': 'Name',
                'foreignField': 'filmTitle',
                'as': 'showings'
            }
        },
        {
            '$match': {
                '$or': [
                    {'Name': {'$regex': search_query, '$options': 'i'}},
                    {'showings.filmTitle': {'$regex': search_query, '$options': 'i'}},
                ]
            }
        },
        {
            '$project': {
                '_id': 1,
                'Name': 1,
                'Rating': 1,
                'Duration': 1,
                'TrailerDescription': 1,
                'showings.filmTitle': 1,

            }
        }
    ]


    result = client['test']['Films'].aggregate(pipeline)

    data = [doc for doc in result]
  
    context = {
        'cursor': cursor,
        'search_query': search_query,
        'data': data,
    }
    return render(request, 'cust/films_list.html', context)