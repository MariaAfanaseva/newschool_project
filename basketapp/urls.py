from basketapp.views import BasketView, BasketAdd, BasketDelete
from django.urls import path

app_name = 'basketapp'

urlpatterns = [
    path('', BasketView.as_view(), name='index'),
    path('add/<int:pk>/', BasketAdd.as_view(), name='add'),
    path('delete/<int:pk>/', BasketDelete.as_view(), name="delete"),
]
