from celery import Task
from accounts.services.send_email_verification import VerifyEmailData
from project_management.celery import app


class SendEmaildIDVerifyEmail(Task):
    """Task for email id verification email send with celery"""
    
    name = "send_email_id_verification_email"

    def run(self, current_site, user_id):
        try:
            VerifyEmailData.send_registration_verify_email(current_site, user_id)
        except Exception as e:
            print(e)

send_email_id_verification_email = app.register_task(SendEmaildIDVerifyEmail())