from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from django.utils.timezone import now
from django.utils import timezone

# Create your models here.
def current_year():
    return datetime.date.today().year

def min_year():
    return current_year() - 4

class House(models.Model):
    STATUS = [
        ('populat', 'Populat'),
        ('depopulat', 'Depopulat'),
        ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='houses')
    name = models.CharField(max_length=100)
    leader_year = models.DateField(
        #blank=True, null=True,
        validators=[
            MinValueValidator(datetime.date(min_year(), 1, 1)),
            MaxValueValidator(datetime.date(current_year(), 12, 31))
            ]
        )
    location = models.CharField(blank=True, null=True, max_length=100)
    rating = models.PositiveIntegerField(
        #blank=True, null=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=1)
    history = models.TextField(default="") # editable=False,
    status = models.CharField(max_length=10, choices=STATUS, default='populat')
    bifata = models.BooleanField(default=False)
    class Meta:
        unique_together = ('user', 'name')
        ordering = ['-leader_year']

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class Todo(models.Model): # Sarcini-planificari
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='todos')
    description = models.TextField(blank=True, null=True, default='')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.description[:20]} ({self.user.username})"

class Operatiune(models.Model): # Contabil
    TIPURI_OPERATIUNI = [
        ('venit', 'Venit'),
        ('cheltuiala', 'Cheltuială'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operatiuni')
    tip = models.CharField(max_length=12, choices=TIPURI_OPERATIUNI)
    suma = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    descriere = models.CharField(max_length=255, blank=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tip.capitalize()}: {self.suma:.2f} lei — {self.data.strftime('%d-%m-%Y')}"

class Pastoral(models.Model): # Deplasari
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pastoral')
    data = models.DateTimeField()
    nr_familii = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(500)])
    destinatie = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.data.strftime('%d-%m-%Y')}: {self.nr_familii} — {self.destinatie}"
