from django.urls import path

from .views import MpWebhookView
urlpatterns = [
    path('mercadopago/test', MpWebhookView.as_view(), name='mp_webhook'),
]