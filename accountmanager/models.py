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

    return cl.find()

def delete(target):
    client = pymongo.MongoClient('mongodb+srv://nathan2miller:hj86z7mW3ZnWG1HH@uweflix.l8xahep.mongodb.net/?retryWrites=true&w=majority')
    db = client['test']
    cl = db["Accounts"]
    cl.delete_one({"id" : target})

def edit(target, change, newdata):
    client = pymongo.MongoClient('mongodb+srv://nathan2miller:hj86z7mW3ZnWG1HH@uweflix.l8xahep.mongodb.net/?retryWrites=true&w=majority')
    db = client['test']
    cl = db["Accounts"]
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
    client = pymongo.MongoClient('mongodb+srv://nathan2miller:hj86z7mW3ZnWG1HH@uweflix.l8xahep.mongodb.net/?retryWrites=true&w=majority')
    db = client['test']
    cl = db["Accounts"]
    firstName = request.POST.get('firstName')
    surname = request.POST.get('surname')
    password = request.POST.get('password')
    cardNumber = request.POST.get('cardNumber')
    expiryDate = request.POST.get('expiryDate')
    discount = request.POST.get('discount')
    DOB = request.POST.get('DOB')
    Type = request.POST.get('Type')
    count = cl.count_documents({}) + 1
    newguy = {"id": count, "Password" : password, "CardNumber" : cardNumber, "DiscountRate" : discount, "ExpiryDate" : expiryDate, "FirstName" : firstName, "LastName" : surname, "Type" : Type, "DOB" : DOB}
    cl.insert_one(newguy)

def dataStatements():
    client = pymongo.MongoClient('mongodb+srv://nathan2miller:hj86z7mW3ZnWG1HH@uweflix.l8xahep.mongodb.net/?retryWrites=true&w=majority')
    db = client['test']
    cl = db["Bookings"]
    cursor = cl.find()
    cl = db["Showings"]
    cursor2 = cl.find()
    cl = db["Accounts"]
    cursor3 = cl.find()

    pipeline = [
            {
                '$lookup': {
                    'from': 'Showings',
                    'localField': 'ShowingID',
                    'foreignField': '_id',
                    'as': 'showings'
                }
            },   
            
            {
                '$lookup': {
                    'from': 'Accounts',
                    'localField': 'AccountID',
                    'foreignField': '_id',
                    'as': 'accounts'
                }
            },
            {
                '$lookup': {
                    'from': 'Clubs',
                    'localField': 'accounts._id',
                    'foreignField': 'Club_id',
                    'as': 'clubs'
                }
            },
            {
                '$project': {
                    'NumberOfTickets': 1,
                    'TotalCost': 1,
                    'PaymentMethod': 1,
                    'DateOfTransaction': 1,
                    'filmTitle': 1,
                    'AccountID': 1,
                    'ShowingID': 1,
                    'showings._id': 1,
                    'showings.filmTitle': 1,
                    'showings.showingTime': 1,
                    'showings.date': 1,
                    'accounts._id': 1,
                    'accounts.firstName': "$accounts.firstName",
                    'clubs._id': 1,
                    'clubs.Name': 1,
                }
            }
        ]

    result = client['test']['Bookings'].aggregate(pipeline)

    data = [doc for doc in result]
    print(data)

    #for x in data:
     #   data[x].append(cl.find({ "_showingID" : x.ShowingID }, {"filmTitle":1}))
    return data