from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.forms import ModelForm, SplitDateTimeWidget, Textarea
from django.utils.translation import ugettext_lazy as _


class Tree(models.Model):
    inventory = models.ForeignKey('Inventory',null=True)
    name = models.CharField(max_length=200)
    latin_name = models.CharField(max_length=200)
    height_m = models.IntegerField()
    circuit_cm = models.IntegerField()
    notes = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return self.name + " " + self.notes

class TreeForm(ModelForm):
    class Meta:
        model = Tree
        fields = ['name', 'latin_name', 'height_m', 'circuit_cm', 'notes', 'created_date']
        labels = {
            'name': _('Name'),
        }
        help_texts = {
            'name': _('Choose polish name.'),
        }
        widgets = {
            'notes': Textarea(attrs={'cols': 40, 'rows': 2}),
        }

class Inventory(models.Model):
    author = models.ForeignKey('auth.User',null=True)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    created_date = models.DateTimeField(
            default=timezone.now)
    client_name = models.CharField(max_length=200)

    def __str__(self):
        return self.name + ", klient: " + self.client_name + ", data: " + str(self.created_date)

class InventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ['author', 'name', 'city', 'street', 'code', 'created_date', 'client_name']
        labels = {
            'author': _('Authorek'),
        }
        help_texts = {
            'name': _('Choose Author.'),
        }
        error_messages = {
            'name': {
                'max_length': _("This authors's name is too long."),
            },
        }
