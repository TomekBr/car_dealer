from random import choices

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
# służy do internacjonalizacji I18N
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(blank=True, max_length=30, verbose_name='first name')
    last_name = models.CharField(blank=True, max_length=30, verbose_name='last name')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Brand(models.Model):
    name = models.CharField(max_length=16)


    def __str__(self):
        return self.name



class Model(models.Model):
    brand_id = models.ForeignKey(Brand, on_delete=models.PROTECT)
    name = models.CharField(max_length=16)

    def __str__(self):
        return f" {self.brand_id} {self.name}"

gearbox = [('Automatic', 'Automatic'), ('Manual', 'Manual')]

fuel = [('Diesel', 'Diesel'), ('Gasoline', 'Gasoline'), ('Electric', 'Electric'), ('Hybrid', 'Hybrid')]

body = [('Sedan', 'Sedan'), ('Combi', 'Combi'), ('SUV', 'SUV'), ('Sport', 'Sport')]


class Vehicle(models.Model):
    model_id = models.ForeignKey(Model, on_delete=models.PROTECT)
    body_type = models.CharField(max_length=16, choices=body)
    prod_year = models.CharField(max_length=4)
    color = models.CharField(max_length=16)
    engine = models.DecimalField(decimal_places=1, max_digits=2)
    type_of_fuel = models.CharField(max_length=16, choices=fuel)
    transmission = models.CharField(max_length=16, choices=gearbox)
    vin = models.CharField(max_length=17)
    photo = models.ImageField()

    def __str__(self):
        return f"Model: {self.model_id}, BodyType: {self.body_type}, Production_Year: {self.prod_year}", \
               f"Color: {self.color}, Engine: {self.engine}, Type_of_Fuel: {self.type_of_fuel}", \
               f"Transmission_Id: {self.transmission}, VIN: {self.vin}, Photo: {self.photo}"


class Branch(models.Model):
    address = models.CharField(max_length=39)
    city = models.CharField(max_length=16)
    mobile = models.CharField(max_length=15)
    opening_hours = models.CharField(max_length=39)
    mail = models.EmailField(max_length=39)
    remarks = models.TextField(null=True)

    def __str__(self):
        return f"Address: {self.address} in {self.city}, opening hours: {self.opening_hours}, mobile: {self.mobile}, " \
               f"mail {self.mail}"


class BranchCarAvailability(models.Model):
    Branch_Id = models.ForeignKey(Branch, on_delete=models.PROTECT)
    Vehicle_Id = models.ForeignKey(Vehicle, on_delete=models.PROTECT)

    def __str__(self):
        return f"Branch: {self.Branch_Id} , Car: {self.Vehicle_Id}"


class RentalOffer(models.Model):
    Vehicle_Id = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    BranchCarAvailability_Id = models.ForeignKey(BranchCarAvailability, on_delete=models.PROTECT)
    Categories = models.CharField(max_length=16)
    Description = models.TextField(null=True)
    Deposit = models.DecimalField(decimal_places=2, max_digits=10)
    Price_per_day = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f"Vehicle_Id: {self.Vehicle_Id}, BranchCarAvailability_Id: {self.BranchCarAvailability_Id}", \
        f"Categories: {self.Categories}, Description: {self.Description}", \
        f"Deposit: {self.Deposit}, Price_per_day: {self.Price_per_day}"
