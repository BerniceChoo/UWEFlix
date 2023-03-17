from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.timezone import datetime
import datetime
from .models import Showings,Screen,Booking,PaymentDetails

#the price of each type of tickets
ticketPrices = { "adult": 7.5, "student": 5, "child": 3.5}

#Create view
def home(request):
    return render(request, "cust/base.html")

def selectDate(request):
    #get list of dates of showings and sort them.
    getDates = Showings.objects.values('showingDate').distinct().order_by('showingDate')
    showingDates = []
    for dates in getDates:
        showingDates.append(dates['showingDate'].strftime('%d-%m-%Y'))

    if request.method == "POST":
        #get the selected date
        selectedDate = request.POST['showingDate']
        #pass the date to the booking view
        return redirect('booking',selectedDate=selectedDate)
        
    #load the list of dates into HTML
    return render(request, "cust/showingDates.html",
        {
            'showingDates': showingDates,
        })

def booking(request, selectedDate):
    if request.method == "GET":
        receivedDate = datetime.datetime.strptime(selectedDate, "%d-%m-%Y").date()
        #get movie on selected date.
        getShowings = Showings.objects.filter(showingDate = receivedDate)
        #pass date, movie, and ticket prices into HTML
        return render(request, "cust/booking.html",
        {
            'selectedDate': selectedDate,
            'getShowings': getShowings,
            'ticketPriceAdult': ticketPrices['adult'],
            'ticketPriceStudent': ticketPrices['student'],
            'ticketPriceChild': ticketPrices['child'],
        })
    if request.method == "POST":
        adultQuantity = request.POST['adultQuantity']
        studentQuantity = request.POST['studentQuantity']
        childQuantity = request.POST['childQuantity']
        selectedShowing = request.POST['selectedShowing']

        #get booking from DB based on what the user has selected
        show = Showings.objects.get(id = selectedShowing)

        print(selectedShowing)

        #get cinema screen for selected showing
        screenCap = Screen.objects.get(id=show.screen_id)
        #calculate total number of tickets
        totalTickets = (int(adultQuantity) + int(studentQuantity) + int(childQuantity))

        #if the user hasn't selected any tickets, send them back
        if (totalTickets == 0):
            print("No tickets were selected.")
            return redirect('booking',selectedDate=selectedDate)

        #if the number of tickets the user has selected overflows the screen capacity, then reject booking
        if ((show.ticketsSold + totalTickets) > screenCap.capacity):
            print("Screen insufficient seats available.")
            return redirect('selectDate')

        #direct payment screen
        return redirect('payment',adultQuantity=adultQuantity, studentQuantity=studentQuantity, childQuantity=childQuantity, selectedShowing=selectedShowing)
        
    return redirect('booking',selectedDate=selectedDate)

def payment(request,adultQuantity, studentQuantity, childQuantity, selectedShowing):
    if request.method == "GET":
        #get selected movie
        try:
            show = Showings.objects.get(id=selectedShowing)
        except Showings.DoesNotExist:
            print("didn't find show")
            return redirect('home')

        if show is None:
            print("didn't find show")
            return redirect('home')
        return render(request, "cust/payment.html",
        {
            'show': show,
        })

    if request.method == "POST":

        #get card details from user
        cardholderName = request.POST['cardholderName']
        cardNumber = request.POST['cardNumber']
        expiryDate = request.POST['expiryDate']
        cardType = request.POST['cardType']

        #if payment details have not been used it will save it
        try:
            existingPayment = PaymentDetails.objects.get(existingPayment = PaymentDetails.objects.get(cardholderName=cardholderName, cardNumber=cardNumber, expiryDate=expiryDate, cardType=cardType))
        except PaymentDetails.DoesNotExist:
            newPayment = PaymentDetails(cardholderName=cardholderName,cardNumber=cardNumber,expiryDate=expiryDate,cardType=cardType)
            newPayment.save()
            existingPayment = newPayment

        #get selected movie
        try:
            getShowing = Showings.objects.get(id=selectedShowing)
        except PaymentDetails.DoesNotExist:
            return redirect("home")
            
        #calculate the cost of booking
        totalCost = ((adultQuantity * ticketPrices["adult"]) + (studentQuantity * ticketPrices["student"]) + (childQuantity * ticketPrices["child"]))

        getShowing.ticketsSold += (adultQuantity + studentQuantity + childQuantity)
        getShowing.save()

        #save booking to DB
        newBooking = Booking(showingRef = getShowing, ticketQuantity = (adultQuantity + studentQuantity + childQuantity), totalCost = totalCost, paymentRef=existingPayment)
        newBooking.save()

        #direct home page
        return redirect("home")