from django.db import models
from django.core.exceptions import ValidationError


class New_bookings(models.Model):
    title_name = models.CharField(' Называние', max_length=20)
    title_text = models.TextField('Краткое описание')
    title_main_text = models.TextField('Описание')
    photo = models.URLField('Главная Фотография', null=True, blank=True)
    photo2 = models.URLField('Фотография 2', null=True, blank=True)
    photo3 = models.URLField('Фотография 3', null=True, blank=True)
    photo4 = models.URLField('Фотография 4', null=True, blank=True)
    photo5 = models.URLField('Фотография 5', null=True, blank=True)

    def __str__(self):
        return self.title_name

    class Meta:
        verbose_name = 'Курорт'
        verbose_name_plural = 'Курорттар'


class Booking(models.Model):
    name = models.CharField(max_length=30, verbose_name='Аты')
    phone_number = models.CharField(max_length=20, verbose_name='Телефон номері')
    booking_date = models.DateField(verbose_name='Брондау уақыты')
    resort = models.ForeignKey(New_bookings, on_delete=models.CASCADE, verbose_name='Курорт')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Брондау'
        verbose_name_plural = 'Брондаулар'

    def clean(self):
        existing_booking = Booking.objects.filter(booking_date=self.booking_date, resort=self.resort).exists()
        if existing_booking:
            raise ValidationError("Бұл уақыт бұрыннан брондалған. Басқа күнді таңдаңыз.")


