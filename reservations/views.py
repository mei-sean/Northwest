from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import Airport, Flight, Passenger, Ticket
from decimal import Decimal

from datetime import datetime


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'reservations/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'reservations/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    return render(request, 'reservations/home.html')

@login_required
def welcome(request):
    return render(request, 'reservations/welcome.html')

@login_required
def my_account(request):
    return render(request, 'reservations/my_account.html')

@login_required
def search(request):
    

    if request.method == 'POST':
        #on post we request the airports and date, 
        depart_airport_code = request.POST['depart_airport']
        arrival_airport_code = request.POST['arrival_airport']
        departure_date = request.POST['depart']
        return_date = request.POST.get('return', None) #set to none in case it is one way flight

        tickets = request.POST['tickets']

        if depart_airport_code == arrival_airport_code:
            error_message = "Invalid destination. Please select a different airport."
            airports = Airport.objects.all()
            return render(request, 'reservations/search.html', {'airports': airports, 'error_message': error_message})
        
        
        #we redirect the user to the list of flights based on the searh
        redirect_url = reverse('list_flights') + f'?depart_airport_code={depart_airport_code}&arrival_airport_code={arrival_airport_code}&departure_date={departure_date}&tickets={tickets}'
        if return_date:
            #in case the user did have a return date we include the date
            redirect_url += f'&return_date={return_date}'
        return redirect(redirect_url)
    else:
        #get all airport information and list all of the required information for the search form
        error_message = request.session.pop('error_message', None)
        airports = Airport.objects.all()
        return render(request, 'reservations/search.html', {'airports': airports, 'error_message': error_message})
    

@login_required
def list_flights(request):
    #function to list flights
    if request.method == 'POST':
        depart_flight_id = request.POST['depart_flights[]']
        return_flight_id = request.POST.get('return_flights[]', None)
        tickets = request.GET.get('tickets')
        
        redirect_url = reverse('passenger_info_view', args=[int(tickets)]) + f'?depart_flight_id={depart_flight_id}'
        if return_flight_id:
            redirect_url += f'&return_flight_id={return_flight_id}'
        
        return redirect(redirect_url)
    else:
        depart_airport_code = request.GET.get('depart_airport_code')
        arrival_airport_code = request.GET.get('arrival_airport_code')
        departure_date_str = request.GET.get('departure_date')
        ret_date_str = request.GET.get('return_date')
        
        depart_airport = Airport.objects.get(code=depart_airport_code)
        arrival_airport = Airport.objects.get(code=arrival_airport_code)

        departure_date = datetime.strptime(departure_date_str, '%Y-%m-%d').date()
        

        flights = Flight.objects.filter(
            depart_airport=depart_airport,
            arrival_airport=arrival_airport,
        )

        if ret_date_str:
            return_date = datetime.strptime(ret_date_str, "%Y-%m-%d").date()
            return_flights = Flight.objects.filter(
                
                depart_airport=arrival_airport,
                arrival_airport=depart_airport,
                
            )
            return render(request, 'reservations/flights_list.html', {'flights': flights, 'departure_date': departure_date, 'return_flights': return_flights, 'return_date': return_date})
        else:
            return_flights = None

            return render(request, 'reservations/flights_list.html', {'flights': flights, 'departure_date': departure_date})
        

def calculate_total_cost(depart_flight, return_flight, num_passengers):
    #Calculates the total cost of a ticket based on the flights and number of passengers.
    
    total_cost = Decimal(0)
    
    # Add the cost of the depart flight
    total_cost += Decimal(depart_flight.price)
    
    # Add the cost of the return flight (if there is one)
    if return_flight:
        total_cost += Decimal(return_flight.price)
    
    # Multiply the total cost by the number of passengers
    total_cost *= num_passengers
    
    return total_cost
        
@login_required
def passenger_info_view(request, num_tickets):
    if request.method == 'POST':
        depart_flight_id = request.GET.get('depart_flight_id')
        return_flight_id = request.GET.get('return_flight_id')
        
        depart_flight = Flight.objects.get(id=depart_flight_id)
        print(depart_flight)
        return_flight = Flight.objects.get(id=return_flight_id) if return_flight_id else None
        
        total_cost = calculate_total_cost(depart_flight, return_flight, num_tickets)
        print(total_cost)
        ticket = Ticket.objects.create(user=request.user, depart_flight=depart_flight, return_flight=return_flight, total_cost=total_cost)

        for i in range(1, num_tickets+1):
            first_name = request.POST.get(f'first_name{i}')
            last_name = request.POST.get(f'last_name{i}')
            email = request.POST.get(f'email{i}')
            dob = request.POST.get(f'dob{i}')
            passenger = Passenger.objects.create(first_name=first_name, last_name=last_name, email=email, dob=dob)
            print(f"Creating passenger with first name: {first_name}, last name: {last_name}, email: {email}, dob: {dob}")
            ticket.passengers.add(passenger)
            
        redirect_url = reverse('payment_view', kwargs={'ticket_id': ticket.id})
        return redirect(redirect_url)
    else:
        ticket_range = range(1, num_tickets + 1)
        return render(request, 'reservations/passenger_information.html', {'ticket_range': ticket_range})

@login_required
def payment_view(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)  
    if request.method == 'POST':
        card_number = request.POST['card_number']
        expiration_date = request.POST['expiration_date']
        cvv = request.POST['cvv']
        name = request.POST['name']
        address = request.POST['address']
        
        # update ticket as paid
        ticket = Ticket.objects.get(id=ticket_id)
        ticket.paid = True
        ticket.save()
        
        return HttpResponse("Payment successful!")
    
    else:
        passengers = ticket.passengers.all()
        return render(request, 'reservations/payment.html', {'ticket': ticket, 'passengers': passengers})

@login_required
def manage_reservations(request):
    user_tickets = Ticket.objects.filter(user=request.user, paid=True)
    return render(request, 'reservations/manage_reservations.html', {'tickets': user_tickets})


