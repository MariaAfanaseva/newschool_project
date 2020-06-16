from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.utils.timezone import now, timedelta


def get_verification_key_time():
    return now() + timedelta(hours=24)


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('The Email must be set.')

        if not password:
            raise ValueError('The password must be set.')

        user = self.model(
            email=self.normalize_email(email), name=name,
        )
        user.set_password(password)
        user.save(using=self._db)  # Default database in settings
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email=email,
            name=name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(verbose_name='Name', max_length=128)
    is_active = models.BooleanField(verbose_name='Active user', default=False)
    is_admin = models.BooleanField(verbose_name='Admin', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # Username and password add by default

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin  # All admins are staff


class UserVerify(models.Model):
    """ Model for verify by email """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    verification_key = models.CharField(max_length=128, blank=True)
    verification_key_expires = models.DateTimeField(default=get_verification_key_time)

    def is_verification_key_valid(self):
        if now() <= self.verification_key_expires:
            return True
        else:
            return False
