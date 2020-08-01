from django.db import models
from django.conf import settings
from mainapp.models import Course


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='basket')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='course')

    def __str__(self):
        return f'{self.user.name} {self.course.name}'

    @staticmethod
    def get_total_quantity(user):
        cart = Basket.objects.filter(user=user)
        return len(cart)

    @staticmethod
    def get_items(request):
        basket_items = Basket.objects.filter(user=request.user).all()\
            .select_related('course', 'course__address', 'course__language_course')
        items = []
        for item in basket_items:
            if item.course.count == 0:
                item.delete()
            else:
                items.append(item)
        return items
