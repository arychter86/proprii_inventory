from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
from django import forms
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
        return str(self.id) + "_" +self.name + ", klient: " + self.client_name + ", data: " + str(self.created_date)

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = [ 'name', 'city', 'street', 'code', 'created_date', 'client_name']
        labels = {
            'name': _('Name'),
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
    crown_m = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    created_date = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return str(self.id) + "_" + self.name + "____" + str(self.created_date)


class TreeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TreeForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        #if instance and instance.pk:
        #    self.fields['name'].widget.attrs['readonly'] = True

    class Meta:
        model = Tree
        fields = ['id','name', 'latin_name', 'height_m', 'crown_m', 'notes']
        labels = {
            'name': _('Name'),
        }
        help_texts = {
            'name': _('Choose polish name.'),
        }
        widgets = {
            'notes': forms.Textarea(attrs={'width':'100%','cols': 10, 'rows': 3}),
        }

class TreeImage(models.Model):
    tree = models.ForeignKey('Tree',null=True)
    picture = models.ImageField(upload_to = 'photos/', default = 'no-img.jpg')
    description = models.CharField(max_length=200)
    created_date = models.DateTimeField(
            default=timezone.now)
    @receiver(pre_delete)
    def delete_repo(sender, instance, **kwargs):
        if sender == TreeImage:
            instance.picture.delete(save=True)


class TreeImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TreeImageForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        #if instance and instance.pk:
        #    self.fields['name'].widget.attrs['readonly'] = True

    class Meta:
        model = TreeImage
        fields = ['description', 'created_date']
        labels = {
            'description': _('Description'),
        }

class TreeTrunk(models.Model):
    tree = models.ForeignKey('Tree')
    trunk_cm = models.IntegerField()
    meas_height_cm = models.IntegerField( default='130')
    created_date = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return str(self.id) + "_" + + str(self.trunk_cm) + "__" + str(self.created_date)

class TreeTrunkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TreeTrunkForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        #if instance and instance.pk:
        #    self.fields['name'].widget.attrs['readonly'] = True

    class Meta:
        model = TreeTrunk
        fields = ['tree','trunk_cm', 'meas_height_cm', 'created_date']
