from django.db import models
from django.utils import timezone


class Tree(models.Model):
    name = models.CharField(max_length=200)
    latin_name = models.CharField(max_length=200)
    height_m = models.IntegerField()
    circuit_cm = models.IntegerField()
    notes = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return name + " " + self.notes

class Inventory(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    created_date = models.DateTimeField(
            default=timezone.now)
    client_name = models.CharField(max_length=200)
    def __str__(self):
        return self.name + ", klient: " + client_name + ", data: " + created_date
