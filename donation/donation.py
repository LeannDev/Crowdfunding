from .models import DonationModel

# new donation
def new_donation(data):
    
    try:
        # create a new donation
        new_donation = DonationModel.objects.create(
            name = data['name'],
            email = data['email'],
            text = data['text'],
            donation = data['donation'],
            goal_id = data['id'],
            payment_method = data['payment_method'],
            payment_token = data['payment_token']
        )
    except:
        new_donation = None

    return new_donation