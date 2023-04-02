from django.shortcuts import render, redirect
from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId
from datetime import datetime
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
Films = db.Films
Bookings = db.Bookings


def login(request, message=None):
    
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
            request.session['ClubID'] = str(result['Club_id'])

            return redirect('select-date-cr' )
        else:
            # Document not found
            print(f"No document found with _id.")
            message = "Your login credentials were not found. Please try again."
            return redirect('login-error', message=message)


    context = {
        'search_query': 1,
        'data': 1,
        'message': message,
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



def view_film(request, pk, message=None):
    Showings_id = ObjectId(pk)

    results = Showings.find_one({ "_id" : Showings_id })
    film_name = results["filmTitle"]
    showing_date = results["date"]
    
    regex = re.compile(film_name, re.IGNORECASE)
    query = {'Name': {'$regex': regex}}

    cursor = Films.find(query)




    if request.POST.get('tickets'):
        numb_of_tickets = int(request.POST.get('tickets'))

        tickets_available = results["ticketsLeft"]


        if numb_of_tickets > tickets_available:
            print("not ennough tickets")
            message = (f"There are not enough tickets available.   Tickets Available: {tickets_available} ")
            return redirect('view-film-error',pk=pk , message=message)
        
        elif numb_of_tickets <= tickets_available:


            club_id = ObjectId(request.session['ClubID'])
            price_before = int(numb_of_tickets) * 10
            price_after = price_before * 0.75
            results = Clubs.find_one({'_id': club_id})
            balance = results['Balance']
            print(balance)
            print(price_after)

            if int(balance) < int(price_after):
                return redirect('club_balance' )
            else:
                return redirect('view-booking', pk=pk ,numb_of_tickets=numb_of_tickets)

     


    context = {
        'cursor': cursor,
        'film_id': pk,
        'date': showing_date,
        'message': message,
    }
    return render(request, 'club_rep/view_film.html', context)









def view_booking(request, pk, numb_of_tickets):
    Showings_id = ObjectId(pk)

    results = Showings.find_one({ "_id" : Showings_id })
    film_name = results["filmTitle"]
    showing_date = results["date"]
    showing_id = results["_id"]

    price_before = int(numb_of_tickets) * 10
    price_after = price_before * 0.75
    
    regex = re.compile(film_name, re.IGNORECASE)
    query = {'Name': {'$regex': regex}}

    cursor = Films.find(query)

    if request.POST.get('tickets'):
        numb_of_tickets = int(request.POST.get('tickets'))
        payment = request.POST.get('payment')
        tickets_available = results["ticketsLeft"]
        tickets_sold = results["ticketsSold"]
        tickets_sold = tickets_sold + numb_of_tickets
        tickets_left= tickets_available - numb_of_tickets

        clubrep_id = ObjectId(request.session['UserID'])

        document={"id": results["id"],
                  "ageRating": results["ageRating"],
                  "filmDuration": results["filmDuration"],
                  "filmTitle": results["filmTitle"],
                  "showingTime": results["showingTime"],
                  "ticketsSold": tickets_sold,
                  "trailerDescription": results["trailerDescription"],
                  "date": results["date"],
                  "ticketsLeft": tickets_left,
                }
        
        result = Showings.update_one({'_id': Showings_id},{'$set': document} )

        now = datetime.now()
        #dt_string = now.strftime("%d/%m/%Y")
        #https://www.programiz.com/python-programming/datetime/current-datetime

        

        document2={"AccountID": clubrep_id,
                  "ShowingID": Showings_id,
                  "NumberOfTickets": numb_of_tickets,
                  "TotalCost": price_after,
                  "PaymentMethod": payment,
                  "DateOfTransaction": now,
                }
        
        


        Bookings.insert_one(document2)

        club_id = ObjectId(request.session['ClubID'])

        results = Clubs.find_one({'_id': club_id})
        balance = results['Balance']
        new_balance = int(balance) - int(price_after)

                       
        document={"Balance": new_balance,
                    }
        
        result = Clubs.update_one({'_id': club_id},{'$set': document} )


        if result.modified_count == 1:
            # Document successfully updated
            print(f"Document with _id updated.")
            message = "Your login credentials were not found. Please try again."
            return redirect('view-all-transactions'  )
        else:
            # Document not found
            print(f"No document found with _id.")
            #return redirect('view-film', pk=pk , error ="" )



    context = {
        'cursor': cursor,
        'date': showing_date,
        'showing_id': showing_id,
        'numb_of_tickets': numb_of_tickets,
        'price_before': price_before,
        'price_after': price_after,
    }

    

    return render(request, 'club_rep/booking.html', context)






def view_transactions(request , selected_month=None):

    clubrep_id = ObjectId(request.session['UserID'])

    if request.GET.get('date'):
        selected_month = request.GET.get('date')
        return redirect( 'view-month-transactions', selected_month=selected_month)

    if selected_month:
        print("po")
        print(selected_month)
        selected_month = datetime.strptime(selected_month, "%Y-%m")

        query = {
            "DateOfTransaction": {
            "$gte": selected_month,
            "$lt": selected_month.replace(month=selected_month.month+1)
            },
            "AccountID": {
            "$eq": clubrep_id
            }
        }

        cursor = Bookings.find(query)
        

    else:
        cursor = Bookings.find({"AccountID" : clubrep_id})




    context = {
        'cursor': cursor,
    }
    return render(request, 'club_rep/transactions.html', context)









def club_balance(request):


    club_id = ObjectId(request.session['ClubID'])
    print(club_id)
    
    
                          
    #cursor = Clubs.find({"Number": number})



    #joins 2 collections together and matches the by local and foreign id
    pipeline = [
        {
        '$match': {
            'Club_id': club_id  # Replace <club_id> with the ID of the club you want to filter by
        }
        },

        {
            '$lookup': {
                'from': 'Clubs',
                'localField': 'Club_id',
                'foreignField': '_id',
                'as': 'clubs'
            }
        },
      
        {
            '$project': {
                '_id': 1,
                'FirstName': 1,
                'LastName': 1,
                'DOB': 1,
                'clubs._id': 1,
                'clubs.Name': 1,
                'clubs.HouseNumber': 1,
                'clubs.Street': 1,
                'clubs.City': 1,
                'clubs.PostCode': 1,
                'clubs.TelephoneNumber': 1,
                'clubs.PhoneNumber': 1,
                'clubs.Email': 1,
                'clubs.Balance': 1,
            }
        }
    ]

    result = client['test']['ClubRep'].aggregate(pipeline)

    data = [doc for doc in result]
    print(data)

    if request.POST.get('funds'):
        funds = request.POST.get('funds')


        results = Clubs.find_one({'_id': club_id})
        balance = results['Balance']
        new_balance = int(balance) + int(funds)

                       
        document={"Balance": new_balance,
                    }
        
        result = Clubs.update_one({'_id': club_id},{'$set': document} )


        return redirect( 'club_balance')

    context = {
        'data': data,
    }
    return render(request, 'club_rep/club.html', context)

































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
    