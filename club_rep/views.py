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





def select_date(request):
    if request.session.get('loggedin', False):
    

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
    else:
        return redirect('login')







def showings_list(request, selected_date):

    if request.session.get('loggedin', False):
    

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
    else:
        return redirect('login')




def view_film(request, pk, message=None):
        
    if request.session.get('loggedin', False):
    
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
                message = (f"There are not enough tickets available. \n Tickets Available: {tickets_available} ")
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
                    message = (f"Insufficient balance in club account. \n Club Balance: £{balance} ")
                    return redirect('view-film-error' ,pk=pk , message=message )
                else:
                    return redirect('view-booking', pk=pk ,numb_of_tickets=numb_of_tickets)

        


        context = {
            'cursor': cursor,
            'film_id': pk,
            'date': showing_date,
            'message': message,
        }
        return render(request, 'club_rep/view_film.html', context)
    else:
        return redirect('login')









def view_booking(request, pk, numb_of_tickets):
    if request.session.get('loggedin', False):
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
    else:
        return redirect('login')






def view_transactions(request , selected_month=None):
    if request.session.get('loggedin', False):

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




        pipeline = [
            {
            '$match': {
                'AccountID': clubrep_id

                }

            },

            {
                '$lookup': {
                    'from': 'Showings',
                    'localField': 'ShowingID',
                    'foreignField': '_id',
                    'as': 'showings'
                }
            },
        
            {
                '$project': {
                    '_id': 1,
                    'NumberOfTickets': 1,
                    'TotalCost': 1,
                    'PaymentMethod': 1,
                    'DateOfTransaction': 1,
                    'showings.showingTime': 1,
                    'showings.date': 1,
                    'showings.Screen': 1,
            
                }
            }
        ]

    

        if selected_month:

            pipeline2 = [
            {
            '$match': {
                'AccountID': clubrep_id,
                'DateOfTransaction': {
                    "$gte": selected_month,
                    "$lt": selected_month.replace(month=selected_month.month+1)
                }
            }

            },

            {
                '$lookup': {
                    'from': 'Showings',
                    'localField': 'ShowingID',
                    'foreignField': '_id',
                    'as': 'showings'
                }
            },
        
            {
                '$project': {
                    '_id': 1,
                    'NumberOfTickets': 1,
                    'TotalCost': 1,
                    'PaymentMethod': 1,
                    'DateOfTransaction': 1,
                    'showings.showingTime': 1,
                    'showings.date': 1,
                    'showings.Screen': 1,
            
                }
            }
        ]
            
            result = client['test']['Bookings'].aggregate(pipeline2)
        else:
            result = client['test']['Bookings'].aggregate(pipeline)

        data = [doc for doc in result]
        print(data)




        context = {
            'cursor': cursor,
            'data': data,
        }
        return render(request, 'club_rep/transactions.html', context)
    else:
        return redirect('login')









def club_balance(request ):
    if request.session.get('loggedin', False):


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

        result = client['test']['Accounts'].aggregate(pipeline)

        data = [doc for doc in result]
        #print(data)

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
    else:
        return redirect('login')



def user_logout(request):
    del request.session['loggedin']
    namey2 = request.session['Name']
    print(namey2)
    del request.session['UserID']
    del request.session['Name']
    del request.session['ClubID']
    return redirect('/login/')
    #return redirect('home-page')



