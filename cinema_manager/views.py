from django.shortcuts import render, redirect
from pymongo import MongoClient
import pymongo
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

"""
def edit_club(request, pk):
    club = Club.objects.get(id=pk)
    form = ClubForm(instance=club)

    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES, instance=club)
        if form.is_valid():
            form.save()
            return redirect('clubs-list')

    context = {
        'club': club,
        'form': form,
    }
    return render(request, 'cinema_manager/edit.html', context)

def delete_club(request, pk):
    club = Club.objects.get(id=pk)

    if request.method == 'POST':
        club.delete()
        return redirect('clubs-list')

    context = {
        'club': club,
    }
    return render(request, 'cinema_manager/delete.html', context)
    """