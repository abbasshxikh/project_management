from accounts.constants import SUCCESS_REGISTRATION_MESSAGE
from accounts.services.email_service import EmailSend


class SuccessEMail:
    """send email after successfully registration"""

    @classmethod
    def send_success_registration_email(cls, user_first_name, to_email):
        message = SUCCESS_REGISTRATION_MESSAGE.get("title").replace(
            "FirstName", user_first_name.capitalize()
        ) + SUCCESS_REGISTRATION_MESSAGE.get("body")

        send_email = EmailSend.send(
            SUCCESS_REGISTRATION_MESSAGE.get("subject"), message, [to_email]
        )
        return send_email
