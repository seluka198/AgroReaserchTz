from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.gis.db import models
from django.conf import settings


# Custom User Manager
class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)


# Custom User Model
class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


# EV Charging Station Model
class EVChargingLocation(models.Model):
    station_name = models.CharField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.station_name


# Model to store uploaded photos
class Photo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='photos/')

    def __str__(self):
        return self.title


# Model to store GIS research data
class ResearchData(models.Model):
    title = models.CharField(max_length=200)
    location = models.PointField()
    crop_type = models.CharField(max_length=100, blank=True, null=True)
    soil_data = models.JSONField(blank=True, null=True)
    soil_raster = models.FileField(upload_to='soil_rasters/', blank=True, null=True)
    researcher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='data_za_utafiti')
    date_collected = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.location}"




