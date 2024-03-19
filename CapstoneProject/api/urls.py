from django.urls import path
from api.Views.ParkingView import ParkingView
from api.Views.UserAnalyticsView import UserAnalyticsView
from api.Views.BookingAnalyticsView import BookingAnalyticsView
from api.Views.RevenueAnalyticsView import RevenueAnalyticsView

urlpatterns = [
    path('parking/', ParkingView.as_view(), name='parking'),
    path('user/',UserAnalyticsView.as_view(), name="user_analytics"),
    path('booking/',BookingAnalyticsView.as_view(), name='booking_analytics'),
    path('revenue/',RevenueAnalyticsView.as_view(),name='revenue_analytics')
]
