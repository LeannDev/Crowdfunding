import os
from pathlib import Path
import environ
import requests
import json

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# environ init
env = environ.Env()
# read .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# generate new payment link
def mp_payment_link(data):

    # MercadoPago url for get pay link
    url = env.str('MP_API_URL')

    # body
    payload = json.dumps({
        "back_urls": {
            "failure": f"https://{data['site']}/donate/failure/",
            "pending": f"https://{data['site']}/donate/pending/",
            "success": f"https://{data['site']}/donate/success/"
        },
        "external_reference": data['id'],
        "items": [
            {
                "id": data['id'],
                "category_id": "donation",
                "title": f"{data['donation']} {data['category']} for X",
                "description": data['description'][:36],
                "quantity": 1,
                "unit_price": data['price'],
                "currency_id": "USD"
                #"picture_url": f"https:{data['site']}/media/"
            }
        ],
        "metadata": data
    }, default=str)

    # headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"bearer {env.str('MP_ACCESS_TOKEN')}"
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
        
        return data_json['init_point']

    else:
        return False