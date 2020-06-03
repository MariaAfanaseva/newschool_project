import datetime
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from mainapp.models import (LanguageCourses, Languages,
                            Teachers)


class IndexListView(ListView):
    model = Languages
    template_name = 'mainapp/index.html'
    context_object_name = 'languages'


class LanguageCoursesListView(ListView):
    context_object_name = 'language_courses'
    template_name = 'mainapp/courses_list.html'

    def get_queryset(self):
        pk = self.kwargs['pk']
        self.current_language = get_object_or_404(Languages,
                                                  pk=pk)
        return LanguageCourses.objects.filter(language=pk).\
            filter(course__start_date__gte=datetime.datetime.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_language'] = self.current_language
        context['languages'] = Languages.objects.all()
        return context


class LanguageCourseDetailView(DetailView):
    model = LanguageCourses
    template_name = 'mainapp/language_course_single.html'
    context_object_name = 'lang_course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = Languages.objects.all()
        return context


class TeachersListView(ListView):
    model = Teachers
    template_name = 'mainapp/teachers_list.html'
    context_object_name = 'teachers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = Languages.objects.all()
        return context
