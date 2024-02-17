from . import views
from django.urls import path

app_name= 'tours'

urlpatterns = [
    path('', views.base, name='main'),
    path('booking/', views.booking, name='booking'),
    path('booking/<int:booking_id>/', views.booking_details, name='booking_details'),
    path('register/', views.register, name='register'),
]
