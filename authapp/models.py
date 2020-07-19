from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.utils.timezone import now, timedelta
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import PermissionsMixin


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

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email=email,
            name=name,
            password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(verbose_name='Name', max_length=128)
    is_active = models.BooleanField(verbose_name='Active user', default=False)
    is_staff = models.BooleanField(verbose_name='Staff', default=False)  # a admin user; non super-user
    is_superuser = models.BooleanField(verbose_name='Admin', default=False)  # a superuser

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # Username and password add by default

    def __str__(self):
        return self.email

    @property
    def get_username(self):
        return self.name


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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    surname = models.CharField(verbose_name='Surname', max_length=128, blank=True)
    country = models.CharField(verbose_name='Country', max_length=128, blank=True)
    city = models.CharField(verbose_name='City', max_length=128, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        """

        SIGNAL saves new user profile and update user
        profile when user save and update.

        """
        user = instance
        if created:
            UserProfile.objects.create(user=user)  # create
        else:
            instance.userprofile.save()  # save form

    def __str__(self):
        return self.surname
