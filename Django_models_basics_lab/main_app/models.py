from datetime import date
from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=30)
    email_address = models.EmailField()
    photo = models.URLField()
    birth_date = models.DateField()
    works_full_time = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)  # DateTimeField is correct for created_on


class Department(models.Model):

    class Locations(models.TextChoices):
        SOFIA = "Sofia", "Sofia"
        PLOVDIV = "Plovdiv", "Plovdiv"
        VARNA = "Varna", "Varna"
        BURGAS = "Burgas", "Burgas"

    code = models.CharField(
        max_length=4,
        primary_key=True,
        unique=True,
    )
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    employees_count = models.PositiveIntegerField(
        default=1,  # Default value should be 1 as per the requirement
        verbose_name="Employees Count",
    )
    location = models.CharField(
        max_length=20,
        choices=Locations.choices  # Correct usage of Locations.choices
    )
    last_edited_on = models.DateTimeField(  # Changed to last_edited_on to match your instructions
        auto_now=True,
        editable=False
    )


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Name")
    description = models.TextField(blank=True, verbose_name="Description")
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Budget")
    duration_in_days = models.PositiveIntegerField(blank=True, null=True, verbose_name="Duration in Days")
    estimated_hours = models.FloatField(blank=True, null=True, verbose_name="Estimated Hours")
    start_date = models.DateField(default=date.today, blank=True, verbose_name="Start Date")
    created_on = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Created On")
    last_edited_on = models.DateTimeField(auto_now=True, editable=False, verbose_name="Last Edited On")

    def __str__(self):
        return self.name
