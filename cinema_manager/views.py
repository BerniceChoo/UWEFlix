from django.shortcuts import render, redirect
from pymongo import MongoClient
import pymongo
import datetime

client = pymongo.MongoClient("mongodb+srv://daniel2fernandes:skelJ6UzCVlG36Ei@uweflix.l8xahep.mongodb.net/?retryWrites=true&w=majority")
# database
db = client.test
# collection 
todos = db.todos


def clubs_list(request):

    search_query = ""

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    cursor = todos.find({})
    for document in cursor:
          print(document)

    context = {
        'document': document,
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

"""
def create_club(request):
    form = ClubForm()

    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('clubs-list')

    context = {
        'form': form,
    }
    return render(request, 'cinema_manager/create.html', context)


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