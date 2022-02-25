from .models import Listings

def delete_realtors_data(realtor_email):
    if Listings.objects.filter(realtor=realtor_email).exists():
        Listings.objects.filter(realtor=realtor_email).delete()