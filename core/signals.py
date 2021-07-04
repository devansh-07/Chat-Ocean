from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .models import Contact

@receiver(user_signed_up)
def createProfile(request, user, **kwargs):
    new_user_contact = Contact.objects.create(user=user)
