import json
from django.views import View
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse

from mercadopago.api import payment_status
from donation.models import DonationModel
from goal.models import GoalModel

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
                
                id = force_str(urlsafe_base64_decode(status['external_reference'])) # decode ID
                donation = DonationModel.objects.get(id=int(id)) # search donation
                donation.paid = True # update paid
                donation.save() # save donation
                goal = GoalModel.objects.get(id=donation.goal.id) # search goal
                goal.progress = goal.progress + (goal.price * donation.donation) # update progress
                goal.save() # save goal

        data = {'message': 'success'}
        return JsonResponse(data)

# PayPal webhooks
class WebhookPp(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        
        # get body request
        body = json.loads(request.body)
        
        if body['event_type'] == 'CHECKOUT.ORDER.APPROVED':

            reference_id = body['resource']['purchase_units'][0]['reference_id'] # ID
            id = force_str(urlsafe_base64_decode(reference_id)) # decode ID
            donation = DonationModel.objects.get(id=id) # search donation
            donation.paid = True # update paid
            donation.save() # save donation
            goal = GoalModel.objects.get(id=donation.goal.pk) # search goal
            goal.progress = goal.progress + (goal.price * donation.donation) # update progress
            goal.save() # save goal

        data = {'message': 'success'}
        return JsonResponse(data)