import razorpay
from razorpay_app import models
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from razorpay_app.tasks.payment_success_task import send_payment_success_email
from accounts.utils import get_domain


class PaymentHomeView(APIView):
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request):
        return Response(template_name="payments/payment_home.html")

    def post(self, request):
        name = request.POST.get('name')
        amount = int(request.POST.get('amount')) * 100
        email = request.POST.get('email')

        # create razorpay client instance
        client = razorpay.Client(auth=("rzp_test_uLDbIUhZ5cnD4y", "VV4oxwreajBdOAfnRKkvFYAm"))

        # We have to generate payment_id
        # We have to capture payment by automatic so it is 1
        # Capture is the process by which payments are secured once the payment has been authorized. 
        response_payment = client.order.create({"amount": amount, "currency": "INR", "payment_capture": "1"})

        if response_payment["status"] == "created":
            payment_data = models.Payment(name=name, amount=amount, email=email, order_id=response_payment["id"])
            payment_data.save()

        return Response({"payment": response_payment}, template_name="payments/payment_home.html")


class PaymentSuccessView(APIView):
    renderer_classes = (TemplateHTMLRenderer,)

    def post(self, request):
        response = request.POST

        # We need to check authenticity of the details by verifying the signature
        params_dict = {
            "razorpay_order_id": response["razorpay_order_id"],
            "razorpay_payment_id": response["razorpay_payment_id"],
            "razorpay_signature": response["razorpay_signature"]
        }

        # client instance
        client = razorpay.Client(auth=("rzp_test_uLDbIUhZ5cnD4y", "VV4oxwreajBdOAfnRKkvFYAm"))

        try:
            # call the utility.verify api to verify the signature status
            status = client.utility.verify_payment_signature(params_dict)
            user = models.Payment.objects.get(order_id=response["razorpay_order_id"])
            user.razorpay_payment_id = response["razorpay_payment_id"]
            user.paid = True
            user.save()
            to_email = user.email
            name = user.name.split(" ")[0]
            current_site = get_domain(request)
            send_payment_success_email.delay(to_email, name, current_site)
            return Response({"status": True}, template_name="payments/payment_status.html")
        except:
            return Response({"status": False}, template_name="payments/payment_status.html")
        
