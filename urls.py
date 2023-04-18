from django.urls import path
from accounts.views import register

urlpatterns = [
    # other URL patterns
    path('register/', register, name='register'),
]
