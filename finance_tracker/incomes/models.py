from django.db import models

# Create your models here.
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Define the Source model before the Income model
class Source(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


# Define the Income model
class Income(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.amount} - {self.Source.name}"

    class Meta:
        ordering = ['-date']
