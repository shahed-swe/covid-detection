from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    address = models.CharField(max_length=250)
    profile_image = models.ImageField(upload_to="profile_image/", blank=True)
    is_active = models.BooleanField(default=True)
    is_doctor = models.BooleanField(default=False)
    is_patient= models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    objects = CustomUserManager()

    class Meta:
        ordering = ['date_joined']
        db_table = "base_user"

    def __str__(self):
        return self.first_name + self.last_name


class Doctor(models.Model):
    """this is a doctor user model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

class Patient(models.Model):
    """this is a patient user model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

class CovidTestImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chest_xray = models.ImageField(upload_to="chestXray", blank=True)
    date_entered = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.first_name + ' ' +self.user.last_name +' -> '+str(self.date_entered)

class CovidResultData(models.Model):
    """this model has been created to store the covid-19 scan result"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resnet = models.CharField(max_length=255)
    vgg = models.CharField(max_length=255)
    inception = models.CharField(max_length=255)
    exception = models.CharField(max_length=255)
    covid_result = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' ->' + str(self.pk)







class PatientCondition(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    condition = models.CharField(max_length=120)

    def __str__(self):
        return  '{} -> {}'.format(self.patient.user.first_name, self.condition)