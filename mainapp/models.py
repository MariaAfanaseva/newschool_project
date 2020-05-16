from django.db import models


class Teachers(models.Model):
    name = models.CharField(verbose_name='teacher_name', max_length=128)
    surname = models.CharField(verbose_name='teacher surname', max_length=128)


class Courses(models.Model):
    name = models.CharField(verbose_name='course name', max_length=128)
    short_desc = models.CharField(verbose_name='course short description',
                                  max_length=60, blank=True)
    description = models.TextField(verbose_name='course description')
    price = models.DecimalField(verbose_name='course price', max_digits=8,
                                decimal_places=2, default=0)
    teacher = models.ManyToManyField(Teachers, verbose_name='teacher')
    date = models.DateTimeField(verbose_name='course date')
