from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_field):
        if not email:
            raise ValueError("Harus Menggunakan Email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_field)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_field):
        extra_field.setdefault("is_staff", False)
        extra_field.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_field)


    def create_superuser(self, email, password=None, **extra_field):
        extra_field.setdefault("is_staff", True)
        extra_field.setdefault("is_superuser", True)
        if extra_field.get("is_staff") is not True:
            raise ValueError(
            "superuser must have is_staff=True"
        )
        if extra_field.get("is_superuser") is not True:
            raise ValueError(
            "superuser must have is_superuser=True"
        )
        return self._create_user(email, password, **extra_field)
        

class User(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    
    def __str__(self):
        return f"{self.email}"


class AuditEntry(models.Model):
    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    username = models.CharField(max_length=256, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):  
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(action='user_logged_in', ip=ip, username=user.email)


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):  
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(action='user_logged_out', ip=ip, username=user.email)


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    AuditEntry.objects.create(action='user_login_failed', username=credentials.get('email', None))