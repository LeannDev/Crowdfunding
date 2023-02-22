from django.urls import path

from .views import DonationAddView

urlpatterns = [
    path('<base64>/', DonationAddView.as_view(), name='donate'),
]