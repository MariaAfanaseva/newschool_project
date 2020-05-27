import datetime
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from mainapp.models import LanguageCourses, Languages


class IndexDetailView(ListView):
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
