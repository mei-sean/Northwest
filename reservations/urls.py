from django.urls import path
from django.contrib.auth import views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('welcome/', views.welcome, name='welcome'),
    path('myaccount/', views.my_account, name='my_account'),
    path("search/", views.search, name="search"),
    path("list_flights", views.list_flights, name='list_flights'),
    path('passenger_info/<int:num_tickets>/', views.passenger_info_view, name='passenger_info_view'),
    path('payment/<int:ticket_id>/', views.payment_view, name='payment_view'),
    path('manage_reservations/', views.manage_reservations, name='manage_reservations'),
]
