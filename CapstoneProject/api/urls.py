from django.urls import path
from . import views

urlpatterns = [
    path('parking/', views.parking, name='parking'),
]
