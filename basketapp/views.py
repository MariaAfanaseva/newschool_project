from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.conf import settings
from mainapp.models import Language, Course
from basketapp.models import Basket


class BasketView(LoginRequiredMixin, View):
    template_name = 'basketapp/index.html'
    login_url = 'auth:login'

    def get(self, request):
        basket_items = Basket.objects.filter(user=request.user)
        client_id = settings.CLIENT_ID

        context = {
            'title': 'Basket',
            'languages': Language.get_languages(),
            'basket_items': basket_items,
            'client_id': client_id,
        }
        return render(request, self.template_name, context)


class BasketAdd(LoginRequiredMixin, View):
    login_url = 'auth:login'

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        basket_course = Basket.objects.filter(user=request.user, course=course).first()

        if not basket_course:
            basket_course = Basket(user=request.user, course=course)

        basket_course.save()

        return HttpResponseRedirect(reverse('basket:index'))


class BasketDelete(LoginRequiredMixin, View):
    login_url = 'auth:login'

    def delete(self, request, pk):
        if request.is_ajax:
            basket_item = Basket.objects.filter(user=request.user, id=pk).first()
            basket_item.delete()
            basket_items = Basket.objects.filter(user=request.user).all()
            context = {'basket_items': basket_items}
            result = render_to_string('basketapp/includes/cart.html', context, request)
            return JsonResponse({'result': result})
