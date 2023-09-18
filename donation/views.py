import uuid

from django.shortcuts import render, redirect
from django.views import View
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
from django.contrib.sites.shortcuts import get_current_site

from DonationsApp.settings import RECAPTCHA_PUBLIC_KEY, RECAPTCHA_SECRET_KEY
from .forms import DonationForm
from goal.models import GoalModel
from .models import DonationModel
from paypal.api import get_access_token, pp_payment_link
from mercadopago.api import mp_payment_link
from .donation import new_donation
from .recaptcha import recaptcha_verify

class DonationAddView(View):

    template_name = 'donation_form.html'
    form_class = DonationForm
    
    def get(self, request, base64):

        # decode id in slug with base64, and search in db
        id = force_str(urlsafe_base64_decode(base64))
        goal = GoalModel.objects.get(id=id)
        
        context = {
            'goal': goal,
            'percentage': (goal.progress * 100) / goal.goal,
            'form': self.form_class,
            'reCAPTCHA_site_key': RECAPTCHA_PUBLIC_KEY,
        }

        return render(request, self.template_name, context)

    def post(self, request, base64):
        
        form = self.form_class(request.POST)
        # decode id in slug with base64, and search in db
        id = force_str(urlsafe_base64_decode(base64))
        goal = GoalModel.objects.get(id=id)
        
        context = {
            'goal': goal,
            'percentage': (goal.progress * 100) / goal.goal,
            'form': self.form_class,
            'reCAPTCHA_site_key': RECAPTCHA_PUBLIC_KEY,
        }

        if form.is_valid():

            # check recaptcha
            recaptcha = request.POST['g-recaptcha-response']
            
            recapthca_values = {
                'secret': RECAPTCHA_SECRET_KEY,
                'response': recaptcha
            }

            verified = recaptcha_verify(recapthca_values)

            if verified['success']:

                data = {
                    'id': base64,
                    'donation': int(form.instance.donation),
                    'name': str(form.instance.name),
                    'email': str(form.instance.email),
                    'text': str(form.instance.text),
                    'title': str(goal.title),
                    'description': str(goal.description),
                    'price': float(goal.price) * int(form.instance.donation),
                    'category': str(goal.category),
                    'payment_method': str(request.POST['pay_method']),
                    'site': str(get_current_site(request)),
                }

                # /////////////////////// CREATE A FUNCTION IN MP AND PP ////////////////////////////////

                # generate new uuid as token
                uuid_token = uuid.uuid4()

                # pay method redirect
                if data['payment_method'] == 'MP':
                    # add new data in dictionary
                    data['payment_token'] = uuid_token
                    data['id'] = int(id)
                    # create a new donation
                    donation = new_donation(data)
                    # add new data in dictionary
                    data['id'] = urlsafe_base64_encode(force_bytes(donation.id))
                    # get MercadoPago pay link
                    pay_link = mp_payment_link(data)

                    if pay_link:
                        # # add new data in dictionary
                        # data['payment_token'] = pay_link['id']
                        # data['id'] = int(id)
                        # # create a new donation
                        # new_donation(data)
                        
                        return redirect(pay_link['init_point'])

                if data['payment_method'] == 'PP':
                    # get or refresh token
                    access_token = get_access_token()
                    # add access token in dict
                    data['access_token'] = access_token
                    # //////////////
                    # add new data in dictionary
                    data['payment_token'] = uuid_token
                    data['id'] = int(id)
                    # create a new donation
                    donation = new_donation(data)
                    # add new data in dictionary
                    data['id'] = urlsafe_base64_encode(force_bytes(donation.id))
                    # /////////////
                    
                    # get PayPal pay link
                    pay_link = pp_payment_link(data)

                    if pay_link:
                        # # add new data in dictionary
                        # data['payment_token'] = pay_link['id']
                        # data['id'] = int(id)
                        # # create a new donation
                        # new_donation(data)

                        return redirect(pay_link['links'][1]['href'])
            
            else:
                # //////////////////////////// RETURN RECAPTCHA ERROR MESSAGE  //////////////////////////////////
                return render(request, self.template_name, context)

        
# /////////////////////////////////// CREATE CSS FOR MESSAGE /////////////////////
# donate success
class DonateSuccessView(View):

    template_name = 'success.html'

    def get(self, request, base64):

        try:
            # decode id in slug with base64, and search in db
            id = force_str(urlsafe_base64_decode(base64))
            donation = DonationModel.objects.get(id=id)
            percentage = (donation.goal.progress * 100) / donation.goal.goal

        except:
            donation = None
            percentage = None

        context = {
            'donation': donation,
            'percentage': percentage,
        }

        return render(request, self.template_name, context)
    
# donate failure
class DonateFailureView(View):

    template_name = 'failure.html'

    def get(self, request, base64):

        try:
            # decode id in slug with base64, and search in db
            id = force_str(urlsafe_base64_decode(base64))
            donation = DonationModel.objects.get(id=id)
            percentage = (donation.goal.progress * 100) / donation.goal.goal

        except:
            donation = None
            percentage = None

        context = {
            'donation': donation,
            'percentage': percentage,
        }

        return render(request, self.template_name, context)
    
# donate pending
class DonatePendingView(View):

    template_name = 'pending.html'

    def get(self, request, base64):

        try:
            # decode id in slug with base64, and search in db
            id = force_str(urlsafe_base64_decode(base64))
            donation = DonationModel.objects.get(id=id)
            percentage = (donation.goal.progress * 100) / donation.goal.goal

        except:
            donation = None
            percentage = None

        context = {
            'donation': donation,
            'percentage': percentage,
        }

        return render(request, self.template_name, context)
    
# view for share donations in social networks
class DonateShareView(View):

    template_name = 'donation_share.html'

    def get(self, request, uuid):

        try:
            # search in db for uuid
            donation = DonationModel.objects.get(payment_token=uuid)
            percentage = (donation.goal.progress * 100) / donation.goal.goal
            print('PORCENTAJE ///////', percentage)

        except:
            donation = None
            percentage = None

        context = {
            'donation': donation,
            'percentage': percentage,
        }

        return render(request, self.template_name, context)