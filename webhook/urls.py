from django.urls import path

from .views import WebhookMp

urlpatterns = [
    path('mercadopago/test/', WebhookMp.as_view(), name='mp_webhook'), # CREATE PRODUCTION URL
]