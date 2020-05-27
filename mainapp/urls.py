from django.urls import path
from mainapp.views import LanguageCoursesListView, IndexDetailView

app_name = 'mainapp'

urlpatterns = [
    path('', IndexDetailView.as_view(), name='index'),
    path('language_courses/<int:pk>/', LanguageCoursesListView.as_view(),
         name='language_courses'),
]
