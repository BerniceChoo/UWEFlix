from django.db import models

import pymongo

# Create your models here.
client = pymongo.MongoClient('mongodb+srv://nathan2miller:hj86z7mW3ZnWG1HH@uweflix.l8xahep.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
cl = db["Accounts"]

def linkDatabase(target):
    client = pymongo.MongoClient('mongodb+srv://nathan2miller:hj86z7mW3ZnWG1HH@uweflix.l8xahep.mongodb.net/?retryWrites=true&w=majority')
    db = client['test']
    cl = db[target]
    table = cl.find()
    fullList = []
    for row in table:
        fullList.append(str(row))
        fullList[-1]=fullList[-1].replace("'","")
        fullList[-1]=fullList[-1].replace(",","")
        fullList[-1]=fullList[-1].split(' ')

    #print(fullList)
    processedList = []
    temp = []

    for x in range (len(fullList)):
        #print(fullList[x])
        temp = []
        temp.append(fullList[x][3])
        temp.append(fullList[x][13])
        temp.append(fullList[x][15].replace("}",""))
        temp.append(fullList[x][11])
        temp.append(fullList[x][7])
        temp.append(fullList[x][9])
        processedList.append(temp)
    return(processedList)     

def delete(target):
    cl.delete_one({"id" : target})

def edit(target, change, newdata):
    print(target)
    print(change)
    print(newdata)
    print("AAAAAAAA")
    target = int(target)
    update = { "id" : target }
    update2 = { "$set" : { change : newdata } }
    cl.update_one(update, update2)
    print(target)
    print(newdata)
    print("AAAAAAAA")

def add(request):    
    firstName = request.POST.get('firstName')
    surname = request.POST.get('surname')
    password = request.POST.get('password')
    cardNumber = request.POST.get('cardNumber')
    expiryDate = request.POST.get('expiryDate')
    discount = request.POST.get('discount')
    count = cl.count_documents({}) + 1
    newguy = {"id": count, "Password" : password, "CardNumber" : cardNumber, "ExpiryDate" : expiryDate, "DiscountRate" : discount, "FirstName" : firstName, "LastName" : surname}
    cl.insert_one(newguy)