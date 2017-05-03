from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.forms import ModelForm, SplitDateTimeWidget, Textarea, HiddenInput
from django.utils.translation import ugettext_lazy as _

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
            'author': _('Author'),
        }
        help_texts = {
            'name': _('Choose Author.'),
        }
        error_messages = {
            'name': {
                'max_length': _("This authors's name is too long."),
            },
        }


class Tree(models.Model):
    inventory = models.ForeignKey('Inventory')
    name = models.CharField(max_length=200)
    latin_name = models.CharField(max_length=200)
    height_m = models.IntegerField()
    circuit_cm = models.IntegerField()
    crown_m = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    created_date = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return self.name + " " + self.notes

class TreeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TreeForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        #if instance and instance.pk:
        #    self.fields['name'].widget.attrs['readonly'] = True

    class Meta:
        model = Tree
        fields = ['name', 'latin_name', 'height_m', 'circuit_cm', 'crown_m', 'notes']
        labels = {
            'name': _('Name'),
        }
        help_texts = {
            'name': _('Choose polish name.'),
        }
        widgets = {
            'name' : HiddenInput(),
            'latin_name' : HiddenInput(),
            'height_m' : HiddenInput(),
            'circuit_cm' : HiddenInput(),
            'crown_m' : HiddenInput(),
            'notes' : HiddenInput(),
            'notes': Textarea(attrs={'cols': 40, 'rows': 1}),
        }

class TreeImage(models.Model):
    tree = models.ForeignKey('Tree',null=True)
    description = models.CharField(max_length=200)
    filename = models.CharField(max_length=200)
    picture = models.ImageField(upload_to = 'photos/', default = 'pic_folder/None/no-img.jpg')
    created_date = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return self.filename + " " + self.tree.name
