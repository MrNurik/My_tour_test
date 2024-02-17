from django import forms
from .models import Booking, New_bookings


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'phone_number', 'booking_date', 'resort']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['resort'].queryset = New_bookings.objects.all()
