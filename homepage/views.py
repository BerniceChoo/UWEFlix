from django.shortcuts import render, redirect
from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId
from datetime import datetime
import re
import string
import random
from django.contrib.auth import authenticate, login, logout

client = pymongo.MongoClient("mongodb+srv://daniel2fernandes:skelJ6UzCVlG36Ei@uweflix.l8xahep.mongodb.net/?retryWrites=true&w=majority")
# database
db = client.test
# collection 
Clubs = db.Clubs
Screens = db.Screens
ClubReps = db.ClubRep
Accounts = db.Accounts
Showings = db.Showings
Films = db.Films
Bookings = db.Bookings


def home(request):
    return render(request, 'home/home.html')


def login(request, message=None):
    
    if request.method == 'POST':
        number = int(request.POST.get('id'))
        print(number)
        password = request.POST.get('Password')
        print(password)
        #   number= int(number)
   
        result = Accounts.find_one({"id": number, "Password": password})
        print(result)


        if result:
            if 'CR' in str(result):
                print(f"Club Rep Found.")

                request.session['loggedin'] = True
                request.session['UserID'] = str(result['_id'])
                request.session['Name'] = str(result['FirstName']) + " " + str(result['LastName'])
                request.session['ClubID'] = str(result['Club_id'])
                namey = request.session['Name']
                print(namey)

                return redirect('/4/selectdate/')
            elif 'AM' in str(result):
                print(f"Account Manager Found.")

                request.session['loggedin'] = True
                request.session['UserID'] = str(result['_id'])
                request.session['Name'] = str(result['FirstName']) + " " + str(result['LastName'])

                return redirect('/3/')
            elif 'CM' in str(result):
                print(f"Cinema Manager Found.")

                request.session['loggedin'] = True
                request.session['UserID'] = str(result['_id'])
                request.session['Name'] = str(result['FirstName']) + " " + str(result['LastName'])

                return redirect('/1/')
            elif 'STU' in str(result):
                print(f"Customer Found.")

                request.session['loggedin'] = True
                request.session['UserID'] = str(result['_id'])
                request.session['Name'] = str(result['FirstName']) + " " + str(result['LastName'])

                return redirect('/5/selectdate/')
            
        else: 
            # Document not found
            print("No document found with _id.")
            message = "Your login credentials were not found. Please try again."
            return redirect('login-error', message=message)


    context = {
        'search_query': 1,
        'data': 1,
        'message': message,
    }
    return render(request, 'home/login.html', context)


#def user_logout(request):
    del request.session['loggedin']
    namey2 = request.session['Name']
    print(namey2)
    del request.session['UserID']
    del request.session['Name']
    del request.session['ClubID']
    return redirect('/login/')
    #return redirect('home-page')