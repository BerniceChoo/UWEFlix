from django.shortcuts import render, redirect
from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId
import datetime
import re
import string
import random
from django.contrib.auth import authenticate, login

client = pymongo.MongoClient("mongodb+srv://daniel2fernandes:skelJ6UzCVlG36Ei@uweflix.l8xahep.mongodb.net/?retryWrites=true&w=majority")
# database
db = client.test
# collection 
Clubs = db.Clubs
Screens = db.Screens
ClubReps = db.ClubRep
Showings = db.Showings


def login(request):
    
    if request.method == 'POST':
        number = request.POST.get('number')
        print(number)
        password = request.POST.get('password')
        print(password)
        number= int(number)
   
        result = ClubReps.find_one({"Number": number, "Password": password})


        if result:
            print(f"Document found.")

            request.session['loggedin'] = True
            request.session['UserID'] = str(result['_id'])
            request.session['Name'] = str(result['FirstName']) + " " + str(result['LastName'])

            return redirect('select-date-cr' )
        else:
            # Document not found
            print(f"No document found with _id.")
            return redirect('login', error='Invalid username or password')


    context = {
        'search_query': 1,
        'data': 1,
    }
    return render(request, 'club_rep/login.html', context)




def select_date(request):

    #selected_date = ""
    

    if request.GET.get('date'):
        selected_date = request.GET.get('date')
       
        
        #cursor = Clubs.find({})
        # case insensitive search using regex
        regex = re.compile(selected_date, re.IGNORECASE)
        query = {'Name': {'$regex': regex}}
        cursor = Screens.find(query)


        context = {
            'cursor': cursor,
            'selected_date': selected_date,
        }
        return redirect('showings_list-cr',selected_date )
        
    
    return render(request, 'club_rep/select_date.html')







def showings_list(request, selected_date):
    

    #selected_date = request.GET.get('date')
    #print(selected_date)
    #selected_date = date
    document={"date": selected_date,
                    }

    results = Showings.find(document)

    data = [doc for doc in results]
       
    

    context = {
        'results': results,
        'selected_date': selected_date,
        'data': data,
    }
    return render(request, 'club_rep/showings_list.html', context)



















def create_club(request):

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
        Clubs.insert_one(document)

        return redirect('clubs-list')

    return render(request, 'club_rep/create.html')


def edit_club(request, pk):

    club_id = ObjectId(pk)
   
    
   
    cursor = Clubs.find({"_id" : club_id})
    context = {
        'club': cursor,
    }
    return render(request, 'club_rep/edit.html', context)



def delete_club(request, pk):
    
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
    return render(request, 'club_rep/delete.html', context)
    


def register_club_rep(request, pk):
    club_id = ObjectId(pk)
    # finds the largest number in the number field from the Club reps collection. "-1" specifies that the sort order is descending
    largest_number = ClubReps.find_one(sort=[("Number", -1)])["Number"]
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
                  "Number": number,
                  "Password": password,
                    }
        
        ClubReps.insert_one(document)

        return redirect('clubs-list')

   
    cursor = Clubs.find({"_id" : club_id})
    context = {
        'club': cursor,
    }

    return render(request, 'club_rep/create_club_rep.html', context)



def delete_club_rep(request, pk):
    
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
    return render(request, 'club_rep/delete_club_rep.html', context)










def create_screen(request):

    if request.method == 'POST':
        screensname = request.POST['screenname']
        capacity = request.POST['capacity']

        document={"Name": screensname,
                  "Capacity": capacity,
                  "SocialDistancing": False,
                    }
        Screens.insert_one(document)

        return redirect('screens-list')

    return render(request, 'club_rep/create_screen.html')


def edit_screen(request, pk):

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
    return render(request, 'club_rep/edit_screen.html', context)


def delete_screen(request, pk):
    
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
    return render(request, 'club_rep/delete_screen.html', context)
    