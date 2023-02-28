import json
from django.views import View
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse

from mercadopago.api import payment_status
from donation.models import DonationModel

# MercadoPago webhooks
class WebhookMp(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        
        # get body request
        body = json.loads(request.body)
        
        if body['data']['id']:
            # check payment status
            status = payment_status(body['data'])
        
            if status['status'] == 'approved':
                # decode id
                id = force_str(urlsafe_base64_decode(status['external_reference']))
                donation = DonationModel.objects.get(id=int(id))
                donation.paid = True
                donation.goal.progress = donation.goal.progress + (donation.goal.price * donation.donation)
                donation.save()
                
        data = {'message': 'success'}
        return JsonResponse(data)
