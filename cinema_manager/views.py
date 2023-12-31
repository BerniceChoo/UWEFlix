from django.shortcuts import render, redirect
from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId
import datetime
import re
import string
import random
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from bson.binary import Binary
import io
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64

client = pymongo.MongoClient("mongodb+srv://daniel2fernandes:skelJ6UzCVlG36Ei@uweflix.l8xahep.mongodb.net/?retryWrites=true&w=majority")
# database
db = client.test
# collection 
Clubs = db.Clubs
Screens = db.Screens
ClubReps = db.Accounts
Films = db.Films
Showings = db.Showings
Accounts = db.Accounts



def clubs_list(request):
    if request.session.get('loggedin', False):

        search_query = ""
        

        if request.GET.get('search_query'):
            search_query = request.GET.get('search_query')
        
            
        #cursor = Clubs.find({})
        # case insensitive search using regex
        regex = re.compile(search_query, re.IGNORECASE)
        query = {'$or': [{'Name': {'$regex': regex}},
                        {'FirstName': {'$regex': regex}},
                            {'FirstName': {'$regex': regex}},
                            {'LastName': {'$regex': regex}},
        ]}
        
                            
        cursor = Clubs.find(query)


        cursor2 = ClubReps.find(query)

        #joins 2 collections together and matches the by local and foreign id
        pipeline = [
            {
                '$lookup': {
                    'from': 'Accounts',
                    'localField': '_id',
                    'foreignField': 'Club_id',
                    'as': 'club_reps'
                }
            },
            {
                '$match': {
                    '$or': [
                        {'Name': {'$regex': search_query, '$options': 'i'}},
                        {'club_reps.FirstName': {'$regex': search_query, '$options': 'i'}},
                        {'club_reps.LastName': {'$regex': search_query, '$options': 'i'}}
                    ]
                }
            },
            {
                '$project': {
                    '_id': 1,
                    'Name': 1,
                    'HouseNumber': 1,
                    'Street': 1,
                    'City': 1,
                    'PostCode': 1,
                    'TelephoneNumber': 1,
                    'PhoneNumber': 1,
                    'Email': 1,
                    'club_reps._id': 1,
                    'club_reps.FirstName': 1,
                    'club_reps.LastName': 1,
                    'club_reps.DOB': 1,
                }
            }
        ]

        result = client['test']['Clubs'].aggregate(pipeline)

        data = [doc for doc in result]


        context = {
            'search_query': search_query,
            'data': data,
        }
        return render(request, 'cinema_manager/list.html', context)
    else:
        return redirect('/login/')



def create_club(request):
    if request.session.get('loggedin', False):

        if request.method == 'POST':
            clubname = request.POST['clubname']
            city = request.POST['city']
            street = request.POST['street']
            email = request.POST['email']
            houseno = request.POST['houseno']
            phoneno = request.POST['phoneno']
            postcode = request.POST['postcode']
            telephoneno = request.POST['telephoneno']

            document={"Name": clubname,
                    "City": city,
                    "Street": street,
                    "Email": email,
                    "HouseNumber": houseno,
                    "PhoneNumber": phoneno,
                    "PostCode": postcode,
                    "TelephoneNumber": telephoneno,
                    "Balance": 0,
                        }
            Clubs.insert_one(document)

            return redirect('clubs-list')

        return render(request, 'cinema_manager/create.html')
    else:
        return redirect('/login/')


def edit_club(request, pk):
    if request.session.get('loggedin', False):

        club_id = ObjectId(pk)
    
        if request.method == 'POST':
            clubname = request.POST['clubname']
            city = request.POST['city']
            street = request.POST['street']
            email = request.POST['email']
            houseno = request.POST['houseno']
            phoneno = request.POST['phoneno']
            postcode = request.POST['postcode']
            telephoneno = request.POST['telephoneno']

            document={"Name": clubname,
                    "City": city,
                    "Street": street,
                    "Email": email,
                    "HouseNumber": houseno,
                    "PhoneNumber": phoneno,
                    "PostCode": postcode,
                    "TelephoneNumber": telephoneno,
                        }
            
            result = Clubs.update_one({'_id': club_id},{'$set': document} )

            if result.modified_count == 1:
                # Document successfully updated
                print(f"Document with _id '{club_id}' updated.")
                return redirect('clubs-list')
            else:
                # Document not found
                print(f"No document found with _id '{club_id}'.")

            return redirect('clubs-list')
    
        cursor = Clubs.find({"_id" : club_id})
        context = {
            'club': cursor,
        }
        return render(request, 'cinema_manager/edit.html', context)
    else:
        return redirect('/login/')



def delete_club(request, pk):
    if request.session.get('loggedin', False):
    
        #convert string to objectId (format of mongoDB _id variable)
        club_id = ObjectId(pk)
        

        if request.method == 'POST':

            result = Clubs.delete_one( { "_id" : club_id } )
            if result.deleted_count == 1:
                # Document successfully deleted
                print(f"Document with _id '{club_id}' deleted.")
                return redirect('clubs-list')
            else:
                # Document not found
                print(f"No document found with _id '{club_id}'.")

            return redirect('clubs-list')
        
        cursor = Clubs.find({"_id" : club_id})
        context = {
            'club': cursor,
        }
        return render(request, 'cinema_manager/delete.html', context)
    else:
        return redirect('/login/')
    



#==================================================================================

def register_club_rep(request, pk):
        
    if request.session.get('loggedin', False):
        club_id = ObjectId(pk)
        # finds the largest number in the number field from the Club reps collection. "-1" specifies that the sort order is descending
        largest_number = ClubReps.find_one(sort=[("id", -1)])["id"]
        number = largest_number + 1 

        # define the length of the random string
        length = 10
        # define the pool of characters to choose from
        characters = string.ascii_letters + string.digits
        # generate the random string
        random_string = ''.join(random.choice(characters) for i in range(length))

        password = random_string
    
        if request.method == 'POST':
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            dob = request.POST['dob']

            document={"FirstName": firstname,
                    "LastName": lastname,
                    "DOB": dob,
                    "Club_id": club_id,
                    "id": number,
                    "Password": password,
                    "Type": "CR"
                        }
            
            ClubReps.insert_one(document)

            return redirect('clubs-list')

    
        cursor = Clubs.find({"_id" : club_id})
        context = {
            'club': cursor,
        }

        return render(request, 'cinema_manager/create_club_rep.html', context)
    else:
        return redirect('/login/')




def delete_club_rep(request, pk):

    if request.session.get('loggedin', False):
    
        #convert string to objectId (format of mongoDB _id variable)
        clubrep_id = ObjectId(pk)
        

        if request.method == 'POST':

            result = ClubReps.delete_one( { "_id" : clubrep_id } )
            if result.deleted_count == 1:
                # Document successfully deleted
                print(f"Document with _id '{clubrep_id}' deleted.")
                return redirect('clubs-list')
            else:
                # Document not found
                print(f"No document found with _id '{clubrep_id}'.")

            return redirect('clubs-list')
        
        cursor = ClubReps.find({"_id" : clubrep_id})
        context = {
            'clubrep': cursor,
        }
        return render(request, 'cinema_manager/delete_club_rep.html', context)
    else:
        return redirect('/login/')



#==================================================================================

def screens_list(request):

    if request.session.get('loggedin', False):

        search_query = ""
        

        if request.GET.get('search_query'):
            search_query = request.GET.get('search_query')
        
            
        #cursor = Clubs.find({})
        # case insensitive search using regex
        regex = re.compile(search_query, re.IGNORECASE)
        query = {'Name': {'$regex': regex}}
        cursor = Screens.find(query)

        #joins showings and films collection, soo that we can see if a film is out for a showing, if it is the film cant be deleted
        pipeline = [
            {
                '$lookup': {
                    'from': 'Showings',
                    'localField': 'Name',
                    'foreignField': 'Screen',
                    'as': 'showings'
                }
            },
            {
                '$match': {
                    '$or': [
                        {'Name': {'$regex': search_query, '$options': 'i'}},
                        {'showings.Screen': {'$regex': search_query, '$options': 'i'}},
                    ]
                }
            },
            {
                '$project': {
                    '_id': 1,
                    'Name': 1,
                    'Capacity': 1,
                    'SocialDistancing': 1,
                    'showings.Screen': 1,

                }
            }
        ]


        result = client['test']['Screens'].aggregate(pipeline)

        data = [doc for doc in result]


        context = {
            'cursor': cursor,
            'search_query': search_query,
            'data': data,
        }
        return render(request, 'cinema_manager/screen_list.html', context)
    else:
        return redirect('/login/')



def create_screen(request):
    if request.session.get('loggedin', False):

        if request.method == 'POST':
            screensname = request.POST['screenname']
            capacity = request.POST['capacity']

            document={"Name": screensname,
                    "Capacity": capacity,
                    "SocialDistancing": False,
                        }
            Screens.insert_one(document)

            return redirect('screens-list')

        return render(request, 'cinema_manager/create_screen.html')
    else:
        return redirect('/login/')



def edit_screen(request, pk):
    if request.session.get('loggedin', False):

        screen_id = ObjectId(pk)
    
        if request.method == 'POST':
            screensname = request.POST['screenname']
            capacity = request.POST['capacity']

            socialdistancing = request.POST.get('socialdistancing', False)
            if (socialdistancing == "true"):
                socialdistancing = True
            elif (socialdistancing == "false"):
                socialdistancing = False

            

            document={"Name": screensname,
                    "Capacity": capacity,
                    "SocialDistancing": socialdistancing,
                        }
            
            result = Screens.update_one({'_id': screen_id},{'$set': document} )

            if result.modified_count == 1:
                # Document successfully updated
                print(f"Document with _id '{screen_id}' updated.")
                return redirect('screens-list')
            else:
                # Document not found
                print(f"No document found with _id '{screen_id}'.")

            return redirect('screens-list')
    
        cursor = Screens.find({"_id" : screen_id})
        context = {
            'screen': cursor,
        }
        return render(request, 'cinema_manager/edit_screen.html', context)
    else:
        return redirect('/login/')




def delete_screen(request, pk):
    if request.session.get('loggedin', False):
    
        #convert string to objectId (format of mongoDB _id variable)
        screen_id = ObjectId(pk)
        

        if request.method == 'POST':

            result = Screens.delete_one( { "_id" : screen_id } )
            if result.deleted_count == 1:
                # Document successfully deleted
                print(f"Document with _id '{screen_id}' deleted.")
                return redirect('screens-list')
            else:
                # Document not found
                print(f"No document found with _id '{screen_id}'.")

            return redirect('screens-list')
        
        cursor = Screens.find({"_id" : screen_id})
        context = {
            'screen': cursor,
        }
        return render(request, 'cinema_manager/delete_screen.html', context)
    else:
        return redirect('/login/')
    


#==================================================================================


def films_list(request):
    if request.session.get('loggedin', False):

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
        return render(request, 'cinema_manager/film_list.html', context)
    else:
        return redirect('/login/')


def create_film(request):
    if request.session.get('loggedin', False):

        if request.method == 'POST':
            filmname = request.POST['filmname']
            agerating = request.POST['agerating']
            duration = request.POST['duration']
            trailerdesc = request.POST['trailerdesc']

            document={"Name": filmname,
                    "Rating": agerating,
                    "Duration": duration,
                    "TrailerDescription": trailerdesc,
                        }
            Films.insert_one(document)

            return redirect('films-list')

        return render(request, 'cinema_manager/create_film.html')
    else:
        return redirect('/login/')



def edit_film(request, pk):
    if request.session.get('loggedin', False):

        film_id = ObjectId(pk)
    
        if request.method == 'POST':
            filmname = request.POST['filmname']
            agerating = request.POST['agerating']
            duration = request.POST['duration']
            trailerdesc = request.POST['trailerdesc']

            

            document={"Name": filmname,
                    "Rating": agerating,
                    "Duration": duration,
                    "TrailerDescription": trailerdesc,
                        }
            
            result = Films.update_one({'_id': film_id},{'$set': document} )

            if result.modified_count == 1:
                # Document successfully updated
                print(f"Document with _id '{film_id}' updated.")
                return redirect('films-list')
            else:
                # Document not found
                print(f"No document found with _id '{film_id}'.")

            return redirect('films-list')
    
        cursor = Films.find({"_id" : film_id})
        context = {
            'film': cursor,
        }
        return render(request, 'cinema_manager/edit_film.html', context)
    else:
        return redirect('/login/')




def delete_film(request, pk):
    if request.session.get('loggedin', False):
    
        #convert string to objectId (format of mongoDB _id variable)
        film_id = ObjectId(pk)
        

        if request.method == 'POST':

            result = Films.delete_one( { "_id" : film_id } )
            if result.deleted_count == 1:
                # Document successfully deleted
                print(f"Document with _id '{film_id}' deleted.")
                return redirect('films-list')
            else:
                # Document not found
                print(f"No document found with _id '{film_id}'.")
            return redirect('films-list')
        
        cursor = Films.find({"_id" : film_id})
        context = {
            'film': cursor,
        }
        return render(request, 'cinema_manager/delete_film.html', context)
    else:
        return redirect('/login/')
    

def user_logout(request):
    del request.session['loggedin']
    namey2 = request.session['Name']
    print(namey2)
    del request.session['UserID']
    del request.session['Name']
    return redirect('/login/')
    #return redirect('home-page')










def showing_list(request):
    if request.session.get('loggedin', False):

        search_query = ""
        

        if request.GET.get('search_query'):
            search_query = request.GET.get('search_query')
        
            
        #cursor = Clubs.find({})
        # case insensitive search using regex
        regex = re.compile(search_query, re.IGNORECASE)
        query = {'Name': {'$regex': regex}}
        cursor = Showings.find(query)

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
                    'filmTitle': 1,
                    'ageRating': 1,
                    'flimDuration': 1,
                    'TrailerDescription': 1,
                    'showings.filmTitle': 1,

                }
            }
        ]


        result = client['test']['Showings'].aggregate(pipeline)
        results = Showings.find()
        datas = [doc for doc in results]
        data = [doc for doc in result]
    
        context = {
            'cursor': cursor,
            'search_query': search_query,
            'data': data,
            'datas': datas,
        }
        return render(request, 'cinema_manager/showing.html', context)
    else:
        return redirect('/login/')

def select_showing(request):    
    if request.session.get('loggedin', False):

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
        return render(request, 'cinema_manager/select_showing.html', context)
    else:
        return redirect('/login/')

def add_showing(request, pk):
    if request.session.get('loggedin', False):

        film_id = ObjectId(pk)
    
        if request.method == 'POST':
            filmname = request.POST['filmname']
            agerating = request.POST['agerating']
            duration = request.POST['duration']
            trailerdesc = request.POST['trailerdesc']
            showing_date = request.POST['showing_date']
            showing_time = request.POST['showing_time']
            Screen = request.POST['Screen']

            data = Screens.find_one({'Name': Screen})

            Capacity = int(data['Capacity'])
            

            document={"filmTitle": filmname,
                    "ageRating": agerating,
                    "filmDuration": duration,
                    "trailerDescription": trailerdesc,
                    "date": showing_date,
                    "showingTime": showing_time,
                    "Screen": Screen,

                    "ticketsSold":0,
                    "ticketsLeft":Capacity,
                        }
            
            Showings.insert_one(document)

            return redirect('showing-list')
        
    
        cursor = Films.find({"_id" : film_id})
        context = {
            'film': cursor,
        }
        return render(request, 'cinema_manager/add_showing.html', context)
    else:
        return redirect('/login/')
    
def delete_showing(request, pk):
    if request.session.get('loggedin', False):
    
        #convert string to objectId (format of mongoDB _id variable)
        showing_id = ObjectId(pk)
        

        if request.method == 'POST':

            result = Showings.delete_one( { "_id" : showing_id } )
            if result.deleted_count == 1:
                # Document successfully deleted
                print(f"Document with _id '{showing_id}' deleted.")
                return redirect('showing-list')
            else:
                # Document not found
                print(f"No document found with _id '{showing_id}'.")
            return redirect('showing-list')
        
        cursor = Showings.find({"_id" : showing_id})
        context = {
            'film': cursor,
        }
        return render(request, 'cinema_manager/delete_showing.html', context)
    else:
        return redirect('/login/')
    
def edit_showing(request, pk):
    if request.session.get('loggedin', False):

        shoiwng_id = ObjectId(pk)
    
        if request.method == 'POST':
            filmname = request.POST['filmname']
            agerating = request.POST['agerating']
            duration = request.POST['duration']
            trailerdesc = request.POST['trailerdesc']
            showing_date = request.POST['showing_date']
            showing_time = request.POST['showing_time']
            Screen = request.POST['Screen']
            

            document={"filmTitle": filmname,
                    "ageRating": agerating,
                    "filmDuration": duration,
                    "trailerDescription": trailerdesc,
                    "date": showing_date,
                    "showingTime": showing_time,
                    "Screen": Screen,
                        }
            
            result = Showings.update_one({'_id': shoiwng_id},{'$set': document} )

            if result.modified_count == 1:
                # Document successfully updated
                print(f"Document with _id '{shoiwng_id}' updated.")
                return redirect('showing-list')
            else:
                # Document not found
                print(f"No document found with _id '{shoiwng_id}'.")

            return redirect('showing-list')
    
        cursor = Showings.find({"_id" : shoiwng_id})
        context = {
            'showing': cursor,
        }
        return render(request, 'cinema_manager/edit_showing.html', context)
    else:
        return redirect('/login/')