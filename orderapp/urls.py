from django.urls import path
from orderapp.views import CreateOrderView, OrderListView


app_name = 'orderapp'

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create'),
    path('orders/', OrderListView.as_view(), name='order_list'),
]
