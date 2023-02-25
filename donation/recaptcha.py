import requests
import json

def recaptcha_verify(data):
    
    url = 'https://www.google.com/recaptcha/api/siteverify'

    # body
    payload = f'secret={data["secret"]}&response={data["response"]}'

    # header
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # POST requests
    response = requests.request(
        "POST",
        url,
        headers=headers,
        data=payload
    )
    
    if response and response.status_code == 200:

        data_json = json.loads(response.text)
        
        return data_json

    else:
        return False