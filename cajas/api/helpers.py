import binascii
import os

from django.contrib.auth.middleware import get_user

def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()
