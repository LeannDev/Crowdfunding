from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse

from mercadopago.api import payment_status

class WebhookMp(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        print('////////// HEADERS /////////', request.headers)
        body = request.body
        print('////////// BODY //////////', body)
        if body['data']['id']:
            status = payment_status(body['data'])

            print('////// DATA STATUS /////', status)
        
        data = {'message': 'success'}
        return JsonResponse(data)
