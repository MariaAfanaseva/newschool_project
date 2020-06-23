import datetime
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from mainapp.models import (LanguageCourses, Languages,
                            Teachers, Courses)


def get_languages():
    return Languages.objects.all()


class IndexListView(ListView):
    template_name = 'mainapp/index.html'
    context_object_name = 'current_courses'

    def get_queryset(self):
        return Courses.objects.filter(
            start_date__gte=datetime.datetime.now()).order_by("?")[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        context['languages'] = get_languages()
        return context


class LanguageCoursesListView(ListView):
    context_object_name = 'language_courses'
    template_name = 'mainapp/courses_list.html'
    paginate_by = 1

    def get_queryset(self):
        pk = self.kwargs['pk']
        self.current_language = get_object_or_404(Languages,
                                                  pk=pk)
        return LanguageCourses.objects.filter(language=pk).\
            filter(course__start_date__gte=datetime.datetime.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_language'] = self.current_language
        context['languages'] = get_languages()
        context['title'] = 'Language courses'
        return context


class LanguageCourseDetailView(DetailView):
    model = LanguageCourses
    template_name = 'mainapp/language_course_single.html'
    context_object_name = 'lang_course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = get_languages()
        context['title'] = 'Language course'
        return context


class TeachersListView(ListView):
    model = Teachers
    template_name = 'mainapp/teachers_list.html'
    context_object_name = 'teachers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = get_languages()
        context['title'] = 'Teachers'
        return context


class TeacherListView(ListView):
    template_name = 'mainapp/teacher_single.html'
    context_object_name = 'teacher_courses'

    def get_queryset(self):
        teacher_pk = self.kwargs['pk']
        self.teacher = get_object_or_404(Teachers, pk=teacher_pk)
        return Courses.objects.filter(teacher=teacher_pk).\
            filter(start_date__gte=datetime.datetime.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = get_languages()
        context['title'] = 'Teacher'
        context['teacher'] = self.teacher
        return context
