
from django.http import HttpResponseBadRequest
from yookassa import Payment
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


def register(request, booking_id=None):
    if booking_id is None:
        # If booking_id is not provided in the URL, handle this case appropriately
        # For example, redirect the user to another page or display an error message
        # Here, I'm just setting it to a default value for demonstration purposes
        booking_id = 1

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'success.html')
        else:
            messages.error(request, "Бұл уақыт брондалған. Басқа күнді таңдаңыз.")
    else:
        form = BookingForm()

    # Извлечение курорта из формы, если он был выбран
    selected_resort = None
    if 'resort' in request.POST:
        selected_resort_id = request.POST.get('resort')
        selected_resort = get_object_or_404(New_bookings, pk=selected_resort_id)

    # Передача цены выбранного курорта в контекст шаблона
    return render(request, 'register.html', {'form': form, 'selected_resort': selected_resort, 'booking_id': booking_id})


def payment(request, booking_id):
    if request.method == 'GET':
        booking = get_object_or_404(New_bookings, pk=booking_id)
        # Создание объекта платежа с учетом цены тура
        payment = Payment.create({
            "amount": {
                "value": str(booking.price),  # Используем цену тура в качестве значения amount
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": request.build_absolute_uri('/payment/success/')
            },
            "description": "Оплата тура"
        })
        # Перенаправление пользователя на страницу оплаты Yookassa
        return redirect(payment.confirmation.confirmation_url)
    else:
        return HttpResponseBadRequest("Invalid request method")


def payment_success(request):
    return render(request, 'success.html')


def payment_result(request):
    # Получаем ID платежа из запроса
    payment_id = request.GET.get('payment_id')
    if payment_id:
        # Получаем информацию о платеже из Yookassa API
        payment = Payment.find_one(payment_id)
        if payment.status == 'succeeded':
            return redirect('payment_success')
        else:
            return render(request, 'payment_result.html', {'payment_success': False})
    else:
        return HttpResponseBadRequest("Invalid payment_id value")

