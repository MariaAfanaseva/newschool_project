import json
import os
from django.core.management.base import BaseCommand
from authapp.models import User
from mainapp.models import (Teacher, Address, Book,
                            Course, LanguageCourse, Language)


JSON_PATH = 'mainapp/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as json_file:
        return json.load(json_file)


def save_teachers():
    teachers = load_from_json('teachers')

    Teacher.objects.all().delete()
    for teacher in teachers:
        new_teacher = Teacher(**teacher)
        new_teacher.save()


def save_addresses():
    addresses = load_from_json('addresses')
    Address.objects.all().delete()
    for address in addresses:
        new_address = Address(**address)
        new_address.save()


def save_books():
    books = load_from_json('books')
    Book.objects.all().delete()
    for book in books:
        new_book = Book(**book)
        new_book.save()


def save_languages():
    languages = load_from_json('languages')
    Language.objects.all().delete()
    for lang in languages:
        new_language = Language(**lang)
        new_language.save()


def save_courses():
    courses = load_from_json('courses')
    Course.objects.all().delete()
    for course in courses:
        street = course['address']
        _address = Address.objects.get(street=street)
        course['address'] = _address

        # get all teachers
        teacher_names = course['teacher'].split(', ')
        teachers = []
        for teacher in teacher_names:
            get_teacher = Teacher.objects.get(name=teacher)
            teachers.append(get_teacher)
        course.pop('teacher')

        new_course = Course(**course)
        new_course.save()
        new_course.teacher.add(*teachers)


def save_language_courses():
    courses = load_from_json('language_courses')
    LanguageCourse.objects.all().delete()
    for course in courses:
        course_name = course['course']
        _get_course = Course.objects.get(name=course_name)
        course['course'] = _get_course

        # get all books
        book_names = course['book'].split(', ')
        books = []
        for book in book_names:
            get_book = Book.objects.get(name=book)
            books.append(get_book)
        course.pop('book')

        language = course['language']
        _language = Language.objects.get(name=language)
        course['language'] = _language

        new_lang_course = LanguageCourse(**course)
        new_lang_course.save()
        new_lang_course.book.add(*books)


class Command(BaseCommand):
    def handle(self, *args, **options):
        save_teachers()
        save_addresses()
        save_books()
        save_languages()
        save_courses()
        save_language_courses()

        print('Recreate manager: ', end='')
        User.objects.all().delete()
        User.objects.create_superuser('admin@admin.com', 'Admin', 'admin')
        print('Done')
