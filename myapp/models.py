from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)  # Name field
    rocnik = models.IntegerField(default=2000)  # Rocnik (Year) field
    description = models.TextField()  # Description field

    def __str__(self):
        return self.name
