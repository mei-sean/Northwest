from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import Airport, Flight, Week

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
    
    if request.method == 'GET': 
        airports = Airport.objects.all()
        return render(request, 'reservations/search.html', {'airports': airports})

    if request.method == 'POST':
        depart_airport_code = request.POST['depart_airport']
        arrival_airport_code = request.POST['arrival_airport']
        departure_date = request.POST['depart']
        return_date = request.POST.get('return', None)
        

        redirect_url = reverse('list_flights') + f'?depart_airport_code={depart_airport_code}&arrival_airport_code={arrival_airport_code}&departure_date={departure_date}'
        if return_date:
            redirect_url += f'&return_date={return_date}'
        return redirect(redirect_url)
    

@login_required
def list_flights(request):
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

    return render(request, 'reservations/flights_list.html', {'flights': flights, 'departure_date': departure_date, 'return_flights': return_flights})

@login_required
def manage_reservations(request):
    return render(request, 'reservations/manage_reservations.html')

