from django.contrib import admin
from orderapp.models import Order, PaymentPayPal


class OrderInline(admin.TabularInline):
    model = Order


@admin.register(PaymentPayPal)
class PaymentPayPalAdmin(admin.ModelAdmin):
    search_fields = 'payer_email',
    list_display = ('payer_email', 'payment_time',)
    inlines = (OrderInline,)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ('user', 'created',)
    list_display = ('user', 'created',)
    list_filter = ('courses',)
