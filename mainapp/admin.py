from django.contrib import admin
from mainapp.models import (
    Course, LanguageCourse,
    Language, Book,
    Address, Teacher
)


class LanguageCourseInline(admin.TabularInline):
    model = LanguageCourse


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = 'name',
    list_filter = ('address__country', 'address__city', 'duration',)
    fields = ['name', 'short_desc', 'description', 'price',
              'teacher', ('start_date', 'finish_date', 'duration'),
              'address', 'image']

    inlines = (LanguageCourseInline,)


@admin.register(LanguageCourse)
class LanguageCourseAdmin(admin.ModelAdmin):
    search_fields = ('course__name',)
    list_display = ('language', 'level_letter', 'level_number',)
    list_filter = ('language', 'level_letter', 'level_number',)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    search_fields = 'name',


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    search_fields = 'name',


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    search_fields = 'city',


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    search_fields = 'name',
