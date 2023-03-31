from django.shortcuts import render

from datetime import datetime

# Create your views here.

from django.http import HttpResponse

import pymongo

client = pymongo.MongoClient('mongodb+srv://nathan2miller:hj86z7mW3ZnWG1HH@uweflix.l8xahep.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
cl = db["Accounts"]

table = cl.find()

print(table)

fullList = []

for row in table:
    fullList.append(str(row))
    fullList[-1]=fullList[-1].replace("'","")
    fullList[-1]=fullList[-1].replace(",","")
    fullList[-1]=fullList[-1].split(' ')

processedList = []
temp = []

for x in range (len(fullList)):
    temp = []
    temp.append(fullList[x][3])
    temp.append(fullList[x][14])
    temp.append(fullList[x][17])
    temp.append(fullList[x][20].replace("}",""))
    processedList.append(temp)


def home(request):
    return HttpResponse("Hello, Django!")

def accountMngrFunc(request):
    return render(
        request,
        'accountmanager/page.html',
        {
            'name': list,
        }
    )

table = cl.find()

print(table)

list = []

for row in table:
    list.append(row)