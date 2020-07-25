import json
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import View
from orderapp.models import PaymentPayPal, Order
from basketapp.models import Basket


class CreateOrderView(View):
    def post(self, request):
        data = json.loads(request.body)
        if data['status'] == 'COMPLETED':
            payment = PaymentPayPal(**data)
            payment.save()

            user = request.user
            courses = Basket.objects.filter(user=user)
            order = Order(user=user, payment_pay_pal=payment)
            order.save()
            for item in courses:
                order.courses.add(item.course)

            courses.delete()

            result = render_to_string('orderapp/order_complete.html')
            return JsonResponse({'result': result})
