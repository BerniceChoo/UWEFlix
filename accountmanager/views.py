from django.shortcuts import render

from datetime import datetime

# Create your views here.

from django.http import HttpResponse

import pymongo

from .models import linkDatabase
from .models import delete
from .models import add
from .models import edit


client = pymongo.MongoClient('mongodb+srv://nathan2miller:hj86z7mW3ZnWG1HH@uweflix.l8xahep.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
cl = db["Accounts"]

def accountMngrTable(request, *args, **kwargs):
    data = linkDatabase("Accounts")
    #print(data)
    my_context = {
        "my_list": data
    }
    return render(request, "accountmanager/viewTable.html", my_context)
    ##return render(
      ##  request,
        ##'accountmanager/page.html',
##        {
  ##          'name': list,
    ##    }
    ##)

#table = cl.find()


##class tablaae():
  ##      template_name = 'table.html'
##
  ##      def get_context_data(request, self, **kwargs):
    ##        ctx = super(table, self).get_context_data(**kwargs)
      ##      ctx['header'] = ['#', 'chemblID','Preferable Name']
        ##    ctx['rows'] = [{'id':1, 'chemblid':534988,'prefName':'A'},
          ##                 {'id':2, 'chemblid':31290,'prefName':'B'},
            ##               {'id':3, 'chemblid':98765,'prefName':'C'}]
            ##return render(request, ""

def accountMngrAdd(request):
    #data = linkDatabase("Accounts")
    #firstName = request.POST.get('firstName')
    #surname = request.POST.get('surname')
    #print(request.POST)
    #print(firstName)
    #print(surname)
    #print("gkhdkfjghdkfgh")
    #newguy = {"id":"3", "Password" : "MYPASSWORD", "Card Number" : "7491039265748283", "Expiry Date" : "1/27", "Discount Rate" : "0", "First Name" : "Zach", "Last Name" : my_title}
    #UHH = cl.insert_one(newguy)

    my_context = {}
    return render(request, "accountmanager/addAccount.html", my_context)

def accountMngrAddRecieved(request):
    #data = linkDatabase("Accounts")
#    firstName = request.POST.get('firstName')
 #   surname = request.POST.get('surname')
  #  password = request.POST.get('password')
   # cardNumber = request.POST.get('cardNumber')
    #expiryDate = request.POST.get('expiryDate')
#    discount = request.POST.get('discount')
 #   print(count)
  #  print(firstName)
   # print(surname)
    #print(password)
#    print(cardNumber)
 #   print(expiryDate)
  #  print(discount)
    print("gkhdkfjghdkfgh")
    add(request)
    my_context = {}
    return render(request, "accountmanager/dataRecievedAdd.html", my_context)

#newguy = {"id":"3", "Password" : "MYPASSWORD", "Card Number" : "7491039265748283", "Expiry Date" : "1/27", "Discount Rate" : "0", "First Name" : "Zach", "Last Name" : my_title}

#x = cl.insert_one(newguy)
#client = pymongo.MongoClient('mongodb+srv://nathan2miller:hj86z7mW3ZnWG1HH@uweflix.l8xahep.mongodb.net/?retryWrites=true&w=majority')
#db = client['test']
#cl = db["Accounts"]

def accountMngrRemove(request, *args, **kwargs):
    data = linkDatabase("Accounts")
    #print(data)
    my_context = {
        "my_list": data
    }
    return render(request, "accountmanager/removeAccount.html", my_context)

def accountMngrEdit(request, *args, **kwargs):
    data = linkDatabase("Accounts")
    #print(data)
    my_context = {
        "my_list": data
    }
    return render(request, "accountmanager/editAccount.html", my_context)

def accountMngrEditRecieved(request):
    #data = linkDatabase("Accounts")
    change = request.POST.get('change')
    number = int(request.POST.get('id'))
    newData = request.POST.get('newData')
    
    filter = { "id" : number }
    update = { "$set" : { change : newData}}
    #UHH = cl.update_one(filter, update)
    #print(UHH)
    edit(number, change, newData)
    
    #UHH = cl.update_one(newguy)
    #update = { "ID" : number }
    #update2 = { "$set" : { change : newData } }
    #clom = cl.update_one({ "ID" : number }, { "$set" : { change : newData } })
    #print(clom)

    #print(filter)
    #print(update)
    print("EditRecieved")

    my_context = {}
    return render(request, "accountmanager/dataRecievedEdit.html", my_context)

def accountMngrRemoveRecieved(request):
    number = int(request.POST.get('id'))
    delete(number)
    print("RemoveRecieved")

    my_context = {}
    return render(request, "accountmanager/dataRecievedRemoved.html", my_context)