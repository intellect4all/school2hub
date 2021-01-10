from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('payment/<ref>/', views.payment, name='payment'),
    path('checkout/flutterwave/verification/', views.FlutterWaveVerification.as_view(), name="flutterwave-verification"),
    path('export/', views.export_page, name="export")
]