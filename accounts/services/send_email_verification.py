from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from accounts.models import User


from accounts.services.email_service import EmailSend


class VerifyEmailData:
    """Send Email to User for email id verification"""

    @classmethod
    def send_registration_verify_email(cls, current_site, user_id):
        user = User.objects.get(pk=user_id)
        token = RefreshToken.for_user(user).access_token
        relativeLink = reverse("accounts:email-verify") 

        absurl = "http://" + current_site + relativeLink + "?token=" + str(token)

        message = 'Hi ' + user.first_name + ' Use link below to verify your email \n' + absurl

        send_email = EmailSend.send_email("Verify your email", message, [user.email])
        return send_email