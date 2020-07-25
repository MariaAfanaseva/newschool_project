from django.db import models
from mainapp.models import Course
from django.conf import settings


class PaymentPayPal(models.Model):
    order_id = models.CharField(max_length=255, verbose_name='id')
    payment_time = models.DateTimeField(verbose_name='payment time')
    status = models.CharField(max_length=255, verbose_name='status')
    payer_email = models.CharField(max_length=255, verbose_name='payer email')
    payer_name = models.CharField(max_length=128, verbose_name='payer name')
    payer_surname = models.CharField(max_length=128, verbose_name='payer surname')

    def __str__(self):
        return self.payer_email


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, related_name='order',
                             blank=True, null=True)
    courses = models.ManyToManyField(Course, verbose_name='courses')
    created = models.DateTimeField(auto_now_add=True)
    payment_pay_pal = models.OneToOneField(PaymentPayPal, on_delete=models.CASCADE,
                                           blank=True, null=True)

    def __str__(self):
        return self.user.email
