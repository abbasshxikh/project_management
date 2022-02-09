import imp
from celery import Task
from accounts.services.welcome_success_email import SuccessEmail
from project_management.celery import app



class SendWelcomeEmail(Task):
    """Task for success registration welcome email after verification with celery"""

    name = "send_welcome_email"

    def run(self, current_site, user_first_name, to_email):
        try:
            return SuccessEmail.send_success_registration_email(current_site, user_first_name, to_email)
        except Exception as e:
            print(e)

send_welcome_email = app.register_task(SendWelcomeEmail())