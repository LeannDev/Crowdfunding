import os
from pathlib import Path
import environ
import requests
import json
from datetime import datetime, timedelta

from .models import PaypalModel

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# environ init
env = environ.Env()
# read .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# get access token
def new_access_token():

    # paypal link
    url = f"{env.str('PP_API_URL')}/v1/oauth2/token"

    # body
    payload = "grant_type=client_credentials"

    # headers
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # response
    response = requests.request("POST", url, auth=(env.str('PP_CLIENT_ID'), env.str('PP_SECRET')), headers=headers, data=payload)
    
    print('RESPONSE', response.status_code)
    if response and response.status_code == 200:

        data_json = json.loads(response.text)

        return data_json

    else:
        return False

def get_access_token():

    # get datetime
    now = datetime.now()
    
    try:
        # search paypal in db
        paypal = PaypalModel.objects.all()[0]
        print('SEARCH TRUE', paypal)

    except:
        # get access token
        requests = new_access_token()
        print('EXCEPT')

        if requests:
            # create access token
            paypal = PaypalModel.objects.create(access_token=requests['access_token'], expires_in=requests['expires_in'])
        
        else:
            paypal = None

    # format datetime db
    updated = paypal.updated_at
    # format and discount expires in
    expires = paypal.updated_at + timedelta(seconds=paypal.expires_in)
    
    # expiration check
    print('UPDATED DATE', updated.strftime('%Y-%m-%d %H:%M:%S'))
    print('EXPIRES DATE', expires.strftime('%Y-%m-%d %H:%M:%S'))
    if now.strftime('%Y-%m-%d %H:%M:%S') >= expires.strftime('%Y-%m-%d %H:%M:%S'):
        print('EXPIRES')
        # if expire get new access token
        new_requests = new_access_token()

        if new_requests:
            # update paypal
            paypal.access_token = new_requests['access_token']
            paypal.expires_in = new_requests['expires_in']
            paypal.save()

            access_token = paypal.access_token

        else:
            access_token = None

    else:
        print('NO EXPIRES')
        access_token = paypal.access_token

    return access_token

# generate new payment link
def pp_payment_link(data):

    # MercadoPago url for get pay link
    url = f"{env.str('PP_API_URL')}/v2/checkout/orders"

    # body
    payload = json.dumps({
        "intent": "CAPTURE",
        "purchase_units": [
            {
            "reference_id": f"{data['id']}",
            "amount": {
                "currency_code": "USD",
                "value": f"{data['price']}"
            }
            }
        ],
        'application_context': {
            "brand_name": f"{data['donation']} {data['category']} for X- {data['site']}", # CHANGE X
            "landing_page": "NO_PREFERENCE",
            "user_action": "PAY_NOW",
            "return_url": f"https:{data['site']}/donate/success/{data['id']}",
            "cancel_url": f"https:{data['site']}/donate/failure/{data['id']}",
            "shipping_preference": "NO_SHIPPING",
        },
    }, default=str)

    # headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {data['access_token']}"
    }

    # POST requests
    response = requests.request(
        "POST",
        url,
        headers=headers,
        data=payload
    )

    if response and response.status_code == 201:

        data_json = json.loads(response.text)

        return data_json

    else:
        return False