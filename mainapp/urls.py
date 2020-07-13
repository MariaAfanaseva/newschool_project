from django.urls import path
from mainapp.views import (LanguageCoursesListView,
                           IndexListView, LanguageCourseView,
                           TeachersListView, TeacherView)

app_name = 'mainapp'

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('language_courses/<int:pk>/', LanguageCoursesListView.as_view(),
         name='language_courses'),
    path('language_course/<int:pk>/', LanguageCourseView.as_view(),
         name='language_course'),
    path('teachers/', TeachersListView.as_view(),
         name='teachers'),
    path('teacher/<int:pk>/', TeacherView.as_view(),
         name='teacher'),
]
