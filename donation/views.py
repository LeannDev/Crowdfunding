from django.shortcuts import render, redirect
from django.views import View
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.sites.shortcuts import get_current_site

from .forms import DonationForm
from goal.models import GoalModel

from paypal.api import get_access_token, pp_payment_link
from mercadopago.api import mp_payment_link
from .donation import new_donation

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
        }

        return render(request, self.template_name, context)

    def post(self, request, base64):

        form = self.form_class(request.POST)
        # decode id in slug with base64, and search in db
        id = force_str(urlsafe_base64_decode(base64))
        goal = GoalModel.objects.get(id=id)
        
        context = {
            'goal': goal,
            'form': self.form_class,
        }

        if form.is_valid():
            
            data = {
                'id': base64,
                'donation': int(form.instance.donation),
                'name': form.instance.name,
                'email': form.instance.email,
                'text': form.instance.text,
                'title': goal.title,
                'description': goal.description,
                'price': float(goal.price) * int(form.instance.donation),
                'category': goal.category,
                'payment_method': request.POST['pay_method'],
                'site': get_current_site(request),
            }

            # pay method redirect
            if data['payment_method'] == 'MP':
                # get MercadoPago pay link
                pay_link = mp_payment_link(data)

                if pay_link:
                    # add new data in dictionary
                    data['payment_token'] = None
                    data['id'] = int(id)
                    # create a new donation
                    new_donation(data)
                    
                    return redirect(pay_link)

            if data['payment_method'] == 'PP':
                # get or refresh token
                access_token = get_access_token()
                # add access token in dict
                data['access_token'] = access_token
                
                # get PayPal pay link
                pay_link = pp_payment_link(data)

                if pay_link:
                    # add new data in dictionary
                    data['payment_token'] = pay_link['id']
                    data['id'] = int(id)
                    # create a new donation
                    new_donation(data)

                    return redirect(pay_link['links'][1]['href'])

        return render(request, self.template_name, context)