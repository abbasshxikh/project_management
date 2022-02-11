from django.template.loader import render_to_string
from accounts.services.password_reset_email_service import email_send
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse

class PaymentSuccess:

    @classmethod
    def send_successful_payment_email(cls, to_email, name, current_site):
        """send email after successful payment"""

        absurl = "http://" + current_site
        relativeLink = reverse("razorpay_app:home") 

        domain = absurl + relativeLink

        html_message =  render_to_string('payments/thank_you.html', {
            "name": name,
            "domain": domain
        })

        message = strip_tags(html_message)

        from_email = settings.EMAIL_HOST_USER
        subject = "Your Donation Has Been Recieved!"
        to_list = [to_email]

        send_email = email_send(subject, message, from_email, to_list, html_message)
        return send_email
