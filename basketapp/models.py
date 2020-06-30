from django.db import models
from django.conf import settings
from mainapp.models import Courses


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='basket')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE,
                               related_name='course')

    def __str__(self):
        return f'{self.user.name} {self.course.name}'
