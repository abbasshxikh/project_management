import imp
from accounts.services.email_service import EmailSend
from accounts.constants import SUCCESS_REGISTRATION_MESSAGE


class SuccessEmail:
    """Send email after verification"""

    @classmethod
    def send_success_registration_email(cls, current_site, user_first_name, to_email):

        message = SUCCESS_REGISTRATION_MESSAGE.get("title").replace(
            "FirstName", user_first_name.capitalize()
        ) + SUCCESS_REGISTRATION_MESSAGE.get("body").replace(
            "current_site", current_site
        )

        send_email = EmailSend.send_email(
            SUCCESS_REGISTRATION_MESSAGE.get("subject"), message, [to_email]
        )
        return send_email