from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

def encode_id(id):
    return urlsafe_base64_encode(force_bytes(id)).decode()