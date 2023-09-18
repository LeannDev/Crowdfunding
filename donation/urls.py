from django.urls import path

from .views import DonationAddView, DonateSuccessView, DonateFailureView, DonatePendingView, DonateShareView

urlpatterns = [
    path('<base64>/', DonationAddView.as_view(), name='donate'),
    path('share/<uuid>/', DonateShareView.as_view(), name='share'),
    path('success/<base64>/', DonateSuccessView.as_view(), name='success'),
    path('failure/<base64>/', DonateFailureView.as_view(), name='failure'),
    path('pending/<base64>/', DonatePendingView.as_view(), name='pending'),
]