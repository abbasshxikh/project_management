import razorpay
from razorpay_app import models
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response


class HomeView(APIView):
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request):
        return Response(template_name="payments/index.html")

    def post(self, request):
        name = request.POST.get('name')
        amount = int(request.POST.get('amount')) * 100
      
        client=razorpay.Client(auth=("rzp_test_uLDbIUhZ5cnD4y", "VV4oxwreajBdOAfnRKkvFYAm"))

        # We have to generate payment_id
        # We have to capture payment by automatic so it is 1
        # Capture is the process by which payments are secured once the payment has been authorized. 
        payment=client.order.create({"amount": amount, "currency": "INR", "payment_capture": "1"})
        payment_data = models.Payment(name=name, amount=amount, order_id=payment["id"])
        payment_data.save()
        return Response({"payment": payment}, template_name="payments/index.html", )


class SuccessView(APIView):
    renderer_classes = (TemplateHTMLRenderer,)

    def post(self, request):
        payment_data = request.POST

        order_id = ""

        # We have to check user payment paid or not via order_id
        for key, val in payment_data.items():
            if key == "razorpay_order_id":
                order_id = val
                break
        user = models.Payment.objects.filter(order_id=order_id).first()
        user.paid = True
        user.save()

        return Response(template_name="payments/success.html")
        
