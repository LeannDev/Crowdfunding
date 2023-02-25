#from django.shortcuts import render
from django.views import View

class MpWebhookView(View):

    def post(self, request):

        print(request)