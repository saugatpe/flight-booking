from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Flight, Passenger
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })

def flight(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    })

def book(request, flight_id):
    if request.method == "POST":
        flight = get_object_or_404(Flight, pk=flight_id)
        try:
            passenger_id = int(request.POST["passenger"])
            passenger = get_object_or_404(Passenger, pk=passenger_id)
            passenger.flights.add(flight)
        except (KeyError, ValueError, Passenger.DoesNotExist):
            return render(request, "flights/flight.html", {
                "flight": flight,
                "passengers": flight.passengers.all(),
                "non_passengers": Passenger.objects.exclude(flights=flight).all(),
                "error_message": "Invalid passenger selected."
            })
        return HttpResponseRedirect(reverse("flight", args=(flight_id,)))
    else:
        return HttpResponseRedirect(reverse("index"))
