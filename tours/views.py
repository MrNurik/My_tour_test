
from .models import New_bookings
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookingForm
from django.contrib import messages


def base(request):
    return render(request, 'index.html')


def booking(request):
    bookings = New_bookings.objects.all()
    return render(request, 'booking.html', {'bookings': bookings})


def booking_details(request, booking_id):
    booking = get_object_or_404(New_bookings, pk=booking_id)
    num_photos = sum(1 for photo in [booking.photo2, booking.photo3, booking.photo4, booking.photo5] if photo)
    return render(request, 'booking_details.html', {'booking': booking, 'num_photos': num_photos})


def register(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'success.html')
        else:
            messages.error(request, "Бұл уақыт брондалған. Басқа күнді таңдаңыз.")
    else:
        form = BookingForm()
    return render(request, 'register.html', {'form': form})


