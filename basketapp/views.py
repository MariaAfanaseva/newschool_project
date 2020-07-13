from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from mainapp.models import Languages, Courses
from basketapp.models import Basket


class BasketView(LoginRequiredMixin, View):
    template_name = 'basketapp/index.html'
    login_url = 'auth:login'

    def get(self, request):
        basket_items = Basket.objects.filter(user=request.user)

        context = {
            'title': 'Basket',
            'languages': Languages.get_languages(),
            'basket_items': basket_items,
        }
        return render(request, self.template_name, context)


class BasketAdd(LoginRequiredMixin, View):
    def get(self, request, pk):
        course = get_object_or_404(Courses, pk=pk)
        basket_course = Basket.objects.filter(user=request.user, course=course).first()

        if not basket_course:
            basket_course = Basket(user=request.user, course=course)

        basket_course.save()

        print(request.META.get('HTTP_REFERER'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class BasketDelete(LoginRequiredMixin, View):
    def get(self, request, pk):
        basket_item = Basket.objects.filter(user=request.user, id=pk).first()
        basket_item.delete()
        basket_items = Basket.objects.filter(user=request.user).all()
        cart_total_quantity = Basket.get_total_quantity(request.user)
        context = {'basket_items': basket_items}

        result = render_to_string('basketapp/includes/cart.html', context, request)
        return JsonResponse({'result': result, 'cart_quantity': cart_total_quantity})
