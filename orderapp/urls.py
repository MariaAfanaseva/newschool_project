from django.urls import path
from orderapp.views import CreateOrderView


app_name = 'orderapp'

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create'),
]
