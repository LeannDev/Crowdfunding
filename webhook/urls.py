from django.urls import path

from .views import WebhookMp, WebhookPp

urlpatterns = [
    path('mercadopago/KewCX69AzTTdnUjivJ3niQn26PBzVG/', WebhookMp.as_view(), name='mp_webhook'),
    path('paypal/QZ7sJNzpEXnRB9tF8soX6PCZgBJd5w/', WebhookPp.as_view(), name='pp_webhook'),
]