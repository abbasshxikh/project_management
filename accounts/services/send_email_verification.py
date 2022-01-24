from accounts.constants import EMAIL_VERIFY_MESSAGE
from accounts.services.email_service import EmailSend


class VerifyEmail:
    """Send Email to User for email id verification"""

    @classmethod
    def send_registration_verify_email(cls, uid, token, first_name, to_email):

        message = (
            EMAIL_VERIFY_MESSAGE.get("title").replace(
                "FirstName", first_name.capitalize()
            )
            + EMAIL_VERIFY_MESSAGE.get("body")
            .replace("UID", uid)
            .replace("TOKEN", token)
            + EMAIL_VERIFY_MESSAGE.get("footer")
        )
        send_email = EmailSend.send(
            EMAIL_VERIFY_MESSAGE.get("subject"), message, [to_email]
        )
        return send_email
