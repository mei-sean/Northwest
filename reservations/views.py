from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import BootstrapAuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Airport
from .forms import BootstrapUserCreationForm

def register(request):
    if request.method == 'POST':
        form = BootstrapUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = BootstrapUserCreationForm()
    return render(request, 'reservations/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = BootstrapAuthenticationForm(data=request.POST)
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
        form = BootstrapAuthenticationForm()
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
        '''depart_airport_code = request.POST['depart_airport']
        destination_airport_code = request.POST['destination_airport']
        departure_date = request.POST['departure_date']
        is_round = request.POST['roundtrip']
        return_date = request.POST.get('return_date', None)

        depart_airport = Airport.objects.get(code=depart_airport_code)
        destination_airport = Airport.objects.get(code=destination_airport_code)

        flights = Flight.objects.filter(
            depart_airport=depart_airport,
            destination_airport=destination_airport,
            departure_date=departure_date,
        )

        if is_round:
            return_flights = Flight.objects.filter(
                depart_airport=destination_airport,
                destination_airport=depart_airport,
                departure_date=request.POST['return_date'],
            )
        else:
            return_flights = None

        return render(request, 'northwest/flights_list.html', {
            'depart_airport': depart_airport,
            'destination_airport': destination_airport,
            'departure_date': departure_date,
            'return_date': return_date,
            'flights': flights,
            'return_flights': return_flights,
        })'''
        return render(request, 'reservations/flights_list.html')

@login_required
def manage_reservations(request):
    return render(request, 'reservations/manage_reservations.html')

