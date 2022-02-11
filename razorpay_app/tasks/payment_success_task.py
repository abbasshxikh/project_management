from celery import Task
from project_management.celery import app
from razorpay_app.services.payment_success_service import PaymentSuccess


class SendPaymentSuccessEmail(Task):
    """Task for password reset email send with celery"""
    
    name = "send_payment_success_email"

    def run(self, to_email, name, current_site):
        try:
            PaymentSuccess.send_successful_payment_email(to_email, name, current_site)
        except Exception as e:
            print(e)

send_payment_success_email = app.register_task(SendPaymentSuccessEmail())


