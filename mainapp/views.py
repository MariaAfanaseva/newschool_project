from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator
from mainapp.models import (LanguageCourse, Language,
                            Teacher, Course, Address
                            )


class CoursesFilter:
    def get_level(self):
        return LanguageCourse.get_level_letter()

    def get_level_number(self):
        return LanguageCourse.get_number_level()

    def get_city(self):
        return Address.get_address_city()


class TeachersFilter:
    def get_country(self):
        return Address.get_address_country()

    def get_city(self):
        return Address.get_address_city()

    def get_language(self):
        return Language.get_languages()


class IndexListView(ListView):
    template_name = 'mainapp/index.html'
    context_object_name = 'current_courses'

    def get_queryset(self):
        return Course.objects.filter(
            start_date__gte=timezone.now()).order_by("?")[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        context['languages'] = Language.get_languages()
        return context


class LanguageCoursesListView(CoursesFilter, ListView):
    context_object_name = 'language_courses'
    template_name = 'mainapp/courses_list.html'
    paginate_by = 3

    def get_queryset(self):
        pk = self.kwargs['pk']
        self.current_language = get_object_or_404(Language,
                                                  pk=pk)
        return LanguageCourse.get_courses(pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_language'] = self.current_language
        context['languages'] = Language.get_languages()
        context['title'] = 'Language courses'
        context['paginator_path'] = self.request.path
        return context


class LanguageCourseView(ListView):
    model = LanguageCourse
    template_name = 'mainapp/language_course_single.html'
    paginate_by = 3

    def get_queryset(self):
        course_pk = self.kwargs['pk']
        self.course = get_object_or_404(LanguageCourse, pk=course_pk)
        language_pk = self.course.language.pk
        return LanguageCourse.get_courses(language_pk).exclude(pk=course_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = Language.get_languages()
        context['title'] = 'Language course'
        context['current_course'] = self.course
        context['paginator_path'] = self.request.path
        return context


class TeachersListView(TeachersFilter, ListView):
    model = Teacher
    template_name = 'mainapp/teachers_list.html'
    context_object_name = 'teachers'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = Language.get_languages()
        context['title'] = 'Teachers'
        context['paginator_path'] = self.request.path
        return context


class TeacherView(ListView):
    template_name = 'mainapp/teacher_single.html'
    context_object_name = 'teacher_courses'
    paginate_by = 3

    def get_queryset(self):
        teacher_pk = self.kwargs['pk']
        self.teacher = get_object_or_404(Teacher, pk=teacher_pk)
        return Course.objects.filter(teacher=teacher_pk).\
            filter(start_date__gte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = Language.get_languages()
        context['title'] = 'Teacher'
        context['teacher'] = self.teacher
        context['paginator_path'] = self.request.path
        return context


class FilterCoursesView(CoursesFilter, ListView):
    template_name = 'mainapp/includes/courses_list.html'

    def _filter_courses(self, request, **kwargs):
        keys = request.GET
        pk = kwargs['pk']
        language = get_object_or_404(Language, pk=pk)
        courses = LanguageCourse.objects.filter(language=language)
        if keys['level_letter']:
            courses = courses.filter(level_letter=str(keys['level_letter']))
        if keys['level_number']:
            courses = courses.filter(level_number=keys['level_number'])
        if keys['city']:
            courses = courses.filter(course__address__city=str(keys['city']))
        return courses

    def get(self, request, *args, **kwargs):
        courses = self._filter_courses(request, **kwargs)
        print(courses)

        paginator = Paginator(courses, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        courses_paginator = paginator.page(page_number)

        context = {
            'language_courses': courses_paginator,
            'paginator_path': request.path,
            'page_obj': page_obj,
            'paginator': paginator,
        }
        result = render_to_string(self.template_name, context, request)
        return JsonResponse({'result': result})


class FilterTeachersView(TeachersFilter, ListView):
    template_name = 'mainapp/includes/teachers_list.html'

    def _filter_teachers(self, request, **kwargs):
        keys = request.GET
        teachers = Teacher.objects.all()
        if keys['city']:
            teachers = teachers.filter(course__address__city=str(keys['city'])).distinct()
        if keys['country']:
            teachers = teachers.filter(course__address__country=keys['country']).distinct()
        if keys['language']:
            teachers = teachers.filter(course__languagecourse__language__name=keys['language'])\
                .distinct()
        return teachers

    def get(self, request, *args, **kwargs):
        teachers = self._filter_teachers(request, **kwargs)

        paginator = Paginator(teachers, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        teachers_paginator = paginator.page(page_number)

        context = {
            'teachers': teachers_paginator,
            'paginator_path': request.path,
            'page_obj': page_obj,
            'paginator': paginator,
        }
        result = render_to_string(self.template_name, context, request)
        return JsonResponse({'result': result})
