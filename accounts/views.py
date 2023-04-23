from django.shortcuts import render
from .forms import UserRegistrationForm

def register(request):
    form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

