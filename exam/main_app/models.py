from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator, MinValueValidator
from .managers import AstronautManager
#Mario1103
class DateTime(models.Model):
    class Meta:
        abstract = True

    creation_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Astronaut(DateTime):
    name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)]
    )
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(regex=r'^\d+$')]
    )
    is_active = models.BooleanField(default=True)
    date_of_birth = models.DateField(null=True, blank=True)
    spacewalks = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    objects = AstronautManager()

    def __str__(self):
        return self.name

class Spacecraft(DateTime):
    name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)]
    )
    manufacturer = models.CharField(
        max_length=100
    )
    capacity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    weight = models.FloatField(
        validators=[MinValueValidator(0.0)]
    )
    launch_date = models.DateField()

    def __str__(self):
        return self.name

class Mission(DateTime):
    PLANNED = 'Planned'
    ONGOING = 'Ongoing'
    COMPLETED = 'Completed'
    STATUS_CHOICES = [
        (PLANNED, 'Planned'),
        (ONGOING, 'Ongoing'),
        (COMPLETED, 'Completed'),
    ]

    name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)]
    )
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=9,
        choices=STATUS_CHOICES,
        default=PLANNED,
    )
    launch_date = models.DateField()
    spacecraft = models.ForeignKey(
        Spacecraft,
        on_delete=models.CASCADE
    )
    astronauts = models.ManyToManyField(Astronaut, related_name='missions')
    commander = models.ForeignKey(
        Astronaut,
        related_name='commanded_missions',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name
