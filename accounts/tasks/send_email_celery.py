from celery import Task
from accounts.services.send_email_verification import VerifyEmail
from project_management.celery_config import celery_app


class SendEmailIdVerifyEmail(Task):
    """task for email id verification email send with celery"""

    name = "send_email_id_verification_email"

    def run(self, uid, token, first_name, to_email):
        # print(uid)
        # print(token)
        # print(first_name)
        # print(to_email)
        try:

            return VerifyEmail.send_registration_verify_email(
                uid, token, first_name, to_email
            )

        except Exception as e:
            print(e)
            # logging.error(
            #     f"Error while calling executing SendEmailIdVerifyEmail. error message: {str(e)}"
            # )
            # return "Failed"


send_email_id_verification_email = celery_app.register_task(SendEmailIdVerifyEmail())


# from django.core.mail import send_mail
# from e_commerce.settings import EMAIL_HOST_USER
# from celery import Task
# from e_commerce.celery_config import celery_app


# class SendEmailTask(Task):

#   name = "send_user_email"


#   def run(self,uid,token,user,first_name ):
#     subject = (f"Thankyou {first_name}")
#     message = "Welcome.."
#     send_mail(subject,message,EMAIL_HOST_USER,[user],
#     fail_silently= False)

#     return send_mail

# send_user_email = celery_app.register_task(SendEmailTask())
