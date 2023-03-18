from django.shortcuts import render, redirect
from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId
import datetime

client = pymongo.MongoClient("mongodb+srv://daniel2fernandes:skelJ6UzCVlG36Ei@uweflix.l8xahep.mongodb.net/?retryWrites=true&w=majority")
# database
db = client.test
# collection 
Clubs = db.Clubs


def clubs_list(request):

    search_query = ""

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    print("lol")

    cursor = Clubs.find({})
    #for document in cursor:
    #      print(document)

    context = {
        'cursor': cursor,
        'search_query': search_query,
    }
    return render(request, 'cinema_manager/list.html', context)



"""
def clubs_list(request):

    search_query = ""

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    clubs = Club.objects.filter(
        Q(club_name__icontains=search_query) | 
        Q(rep_first_name__icontains=search_query) |
        Q(rep_last_name__icontains=search_query)
    )

    context = {
        'clubs': clubs,
        'search_query': search_query,
    }
    return render(request, 'cinema_manager/list.html', context)
"""


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

    context = {
        'form': 1,
    }
    return render(request, 'cinema_manager/create.html', context)


def edit_club(request, pk):

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
   

    context = {
        'club': 1,
        'form': 1,
    }
    return render(request, 'cinema_manager/edit.html', context)



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

    context = {
        'club': 1,
    }
    return render(request, 'cinema_manager/delete.html', context)
    