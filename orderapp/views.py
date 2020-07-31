import json
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import View, ListView
from orderapp.models import PaymentPayPal, Order
from basketapp.models import Basket
from mainapp.models import Language


class CreateOrderView(View):
    def post(self, request):
        data = json.loads(request.body)
        if data['status'] == 'COMPLETED':
            payment = PaymentPayPal(**data)
            payment.save()

            user = request.user
            courses = Basket.objects.filter(user=user)
            order = Order(user=user, payment=payment)
            total_price = 0
            order.save()
            for item in courses:
                total_price += item.course.price
                count = item.course.count
                if count > 0:
                    item.course.count = count - 1
                    item.course.save()
                order.courses.add(item.course)

            courses.delete()
            order.total_price = total_price
            order.save()

            result = render_to_string('orderapp/order_complete.html')
            return JsonResponse({'result': result})


class OrderListView(ListView):
    template_name = 'orderapp/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        orders = Order.objects.filter(user=self.request.user).order_by('-created')
        return orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = Language.get_languages()
        context['title'] = 'Orders'
        return context
