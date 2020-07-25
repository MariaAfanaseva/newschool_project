from django.contrib import admin
from orderapp.models import Order, PaymentPayPal


@admin.register(PaymentPayPal)
class PaymentPayPalInline(admin.ModelAdmin):
    search_fields = 'payer_email',
    list_display = ('payer_email', 'payment_time',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ('user', 'created',)
    list_display = ('user', 'created',)
