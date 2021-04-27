from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponseRedirect
import json
from django.shortcuts import render, redirect
from .models import Bus, Route, Booking, Passenger, Faq, Review, Contact
from django.contrib import messages
from .forms import PassengerForm
from .filter import RouteFilter

from django.views.generic import View
from django.utils import timezone
from .render import Render

# Create your views here.
def home(request):
    #get user review
    review = Review.objects.all().order_by('-date_added')

    #get all buses route
    route = Route.objects.all()

    #filter buses using django filter
    filter = RouteFilter(request.GET, queryset=route)   #filter
    route = filter.qs

    context={'review':review, 'filter':filter, 'route':route}
    return render(request, 'booking/home.html',context)

def route_list(request):
    #get all bus routes
    route = Route.objects.all()

    return render(request, 'booking/route_list.html', {'bus_list': route})


def booking_info(request, pk):
    form = PassengerForm()
    detail = Route.objects.get(id=pk)
    bus_id=detail.bus.id
    bus = Bus.objects.get(id=bus_id)
    
    seats_selected = Passenger.objects.filter(bus=bus)

    total_seat = bus.total_seats

    #function to get number of seat already booked
    b=[]
    def reserverd_seat(x):
        seat_list = []
        for i in seats_selected:
            for a in range(total_seat):
                if a != i.seat_no:
                    pass
                else:
                    seat_list.append(a)
        return seat_list

    reserverd_seat = reserverd_seat(b)

    #function to get number of available empty seat
    c=[]
    def empty_seat(x):
        seat_list = []
        for i in range(1, total_seat+1):
            if i not in reserverd_seat:
                seat_list.append(i)
        return seat_list

    empty_seat = empty_seat(c)

    context = {'detail':detail, 'form':form, 'seats_selected':seats_selected, 'reserverd_seat':reserverd_seat, 'range':range(1,total_seat+1)}
    return render(request, 'booking/booking_info.html', context)


def booking(request):
    if request.method == 'POST':
        form = PassengerForm(request.POST)
        bus_id = request.POST['bus_id']
        bus_name = request.POST['bus_name']
        journey_date = request.POST['dateofjourney']
        departure = request.POST['departure']
        arrival = request.POST['arrival']
        source = request.POST['from']
        destination = request.POST['destination']
        fares = request.POST['fares']
        seat_no = request.POST['seat_no']
        
        if form.is_valid():
            passenger = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            bus = Bus.objects.get(id=bus_id)
            form.instance.bus = bus
            form.instance.seat_no = seat_no
        else:
            messages.warning(request, f'something went wrong during form submission')
            
        
        #seats_selected = Passenger.objects.filter(bus=bus, seat_no=seat_no)
        #if seats_selected:
        #    messages.warning(request, f'sorry seat already reserved, choose another seat')
            #return redirect('home')
        #else:
            
        try:
            #if ticket available then get ticket
            ticket = Booking.objects.get(bus=bus, phone=phone, passenger=passenger, seat_no=seat_no)
        except Booking.DoesNotExist:
            booking = Booking.objects.create(
                passenger=passenger, journey_date=journey_date, bus=bus_name, departure=departure, arrival=arrival,
                source=source, destination=destination, phone=phone, fare=fares, seat_no=seat_no
            )
            form.save()
            booking.save()
            messages.success(request, f'Your booking information saved successfull, Now complete payment below')
            
            #get ticket
            ticket = Booking.objects.get(bus=bus, phone=phone, passenger=passenger, seat_no=seat_no)

        return render(request, 'booking/ticket.html', {'ticket':ticket})
    else:
        return redirect('home')
    #context = {'booking':booking, 'form':form}
    return render(request, 'booking/home.html')


def cancel(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        ticketid = request.POST['ticketid']
        try:
            ticket = Booking.objects.get(phone=phone, passenger=name, id=ticketid)
            ticket.delete()
            
            return render(request, 'booking/cancel.html')
        except Booking.DoesNotExist:
            messages.warning(request, f'sorry no ticket match your ticket, plz.. fill correct info')
    return render(request, 'booking/cancel.html')

def faq(request):
    #get all FAQs
    faq = Faq.objects.all().order_by('-date_added')
    if request.method == 'POST':
        name = request.POST['name']
        question = request.POST['question']
        faq = Faq.objects.create(
            name=name, question=question
        )
        faq.save()
        messages.success(request, f'Your question received, we will answer you in just a moment')
        return redirect('faq')
    return render(request, 'booking/asked_question.html', {'faq':faq})

def review(request):
    if request.method == 'POST':
        name = request.POST['name']
        review = request.POST['review']

        review = Review.objects.create(
            name=name, review=review
        )
        review.save()
        return redirect('home')
    return render(request, 'booking/home.html')


def ticket(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        ticketid = request.POST['ticketid']
        try:
            ticket = Booking.objects.get(phone=phone, passenger=name, id=ticketid)

            context = {'ticket':ticket}
            return render(request, 'booking/ticket.html', context)
        except Booking.DoesNotExist:
            messages.warning(request, f'sorry no ticket match your information, plz.. fill correct information')
    
    return render(request, 'booking/ticket.html')
    #return render(request, 'booking/ticket.html')

def contact(request):
    if request.method =='POST':
        name = request.POST['name']
        message = request.POST['message']

        #uncomment below line if you wanna get email to your email inbox
        
        #send_mail(
         #   'Contact Form',
          #  message,
           # settings.EMAIL_HOST_USER,
            #['jbfrancis60@gmail.com'],
            #fail_silently = False
        #)

        message = Contact.objects.create(
            name = name, message = message
        )
        message.save()
        messages.success(request, f'your message sent successfully...')
        return redirect('home')
    return render(request, 'booking/contact.html')

@csrf_exempt
def complete_payment(request):
    data = json.loads(request.body)
    print('BODY:',data)
    ticketId = data['bookingId']

    ticket = Booking.objects.get(id=ticketId)

    ticket.complete='True'
    ticket.save()
    return JsonResponse('payment complete!', safe=False)

def success_paid(request,pk):
    ticket = Booking.objects.get(id=pk)
    context = {'ticket':ticket}
    return render(request, 'booking/success_paid.html',context)


#download ticket view
class Pdf(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        ticket = Booking.objects.get(id=pk)
        today = timezone.now()

        contenxt = {
            'today': today,
            'ticket': ticket,
        }
        return Render.render('booking/download_ticket.html', contenxt)

def helps(request):
    return render(request, 'booking/helps.html')

def service(request):
    return render(request, 'booking/service.html')