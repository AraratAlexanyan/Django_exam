from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from . import helpers


class AccountManager(BaseUserManager):
    def create_user(self, phone, **extra_fields):
        if not phone:
            raise ValueError("The Email must be set")
        phone = self.normalize_email(phone)
        user = self.model(phone=phone, **extra_fields)
        user.save()
        return user

    def create_superuser(self, phone, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(phone, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=50, blank=False, unique=True)
    is_active = False
    referral_code = models.TextField(blank=True, unique=True)

    objects = AccountManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        self.referral_code = helpers.generate_unique(self)
        super(Account, self).save(*args, **kwargs)

    def __str__(self):
        return self.phone


class Referrals(models.Model):
    user_id = models.ForeignKey('Account', on_delete=models.SET_NULL,
                                blank=True, null=True, related_name='referral', default=None)

    referrals = models.OneToOneField('Account', on_delete=models.SET_NULL, blank=True, null=True,
                                     related_name='recommendations', default=None)
