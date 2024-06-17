from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Define the Category model before the Expense model
class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name


# Define the Expense model
class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.amount} - {self.category.name}"

    class Meta:
        ordering = ['-date']
