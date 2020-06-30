import datetime
from django.db import models


class Teachers(models.Model):
    name = models.CharField(verbose_name='teacher name', max_length=128)
    surname = models.CharField(verbose_name='teacher surname', max_length=128)
    dob = models.DateField(verbose_name='teacher date of birth', null=True)
    education = models.CharField(verbose_name='teacher education', max_length=255, blank=True)
    introduction = models.TextField(verbose_name='teacher introduction text', blank=True)
    about_teacher = models.TextField(verbose_name='about teacher', blank=True)
    photo = models.ImageField(verbose_name='teacher photo', blank=True)

    def __str__(self):
        return f'{self.name} {self.surname}'


class Addresses(models.Model):
    country = models.CharField(verbose_name='country', max_length=128, blank=True)
    city = models.CharField(verbose_name='city', max_length=128, blank=True)
    street = models.CharField(verbose_name='street', max_length=255, blank=True)
    house_number = models.IntegerField(verbose_name='house number', blank=True, null=True)
    floor = models.IntegerField(verbose_name='house floor', blank=True, null=True)
    room_number = models.IntegerField(verbose_name='room number', blank=True, null=True)
    google_map = models.CharField(verbose_name='google map', max_length=500, blank=True)

    def __str__(self):
        return f'{self.country}, {self.city}, {self.street}, {self.house_number}'


class Courses(models.Model):
    name = models.CharField(verbose_name='course name', max_length=128)
    short_desc = models.CharField(verbose_name='course short description',
                                  max_length=60, blank=True)
    description = models.TextField(verbose_name='course description')
    price = models.DecimalField(verbose_name='course price', max_digits=8, decimal_places=2, default=0)
    teacher = models.ManyToManyField(Teachers, verbose_name='teacher', blank=True)
    start_date = models.DateTimeField(verbose_name='course start date', null=True)
    finish_date = models.DateTimeField(verbose_name='course finish date', null=True)
    duration = models.PositiveIntegerField(verbose_name='course duration', default=1)
    address = models.ForeignKey(Addresses, models.SET_NULL,
                                blank=True, null=True,
                                verbose_name='course address')
    image = models.ImageField(verbose_name='course image', blank=True)

    def __str__(self):
        return f'{self.name}'


class Books(models.Model):
    name = models.CharField(verbose_name='book name', max_length=255)
    author = models.CharField(verbose_name='book author', max_length=128)
    description = models.TextField(verbose_name='book description', blank=True)

    def __str__(self):
        return f'{self.name}'


class Languages(models.Model):
    name = models.CharField(verbose_name='language name', max_length=128)
    description = models.TextField(verbose_name='language description')
    is_active = models.BooleanField(verbose_name='active', default=True, db_index=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_languages():
        return Languages.objects.all()


class LanguageCourses(models.Model):
    course = models.OneToOneField(Courses, primary_key=True, on_delete=models.CASCADE)
    language = models.ForeignKey(Languages, models.CASCADE, verbose_name='language')
    level_letter = models.CharField(verbose_name='language level letter', max_length=1)
    level_number = models.FloatField(verbose_name='language level number', max_length=3)
    book = models.ManyToManyField(Books, verbose_name='book')

    def __str__(self):
        return f'{self.language}'

    @staticmethod
    def get_courses(language_pk):
        return LanguageCourses.objects.filter(language=language_pk). \
            filter(course__start_date__gte=datetime.datetime.now())
