from basketapp.views import BasketView
from django.urls import path

app_name = 'basketapp'

urlpatterns = [
    path('', BasketView.as_view(), name='index')
]
