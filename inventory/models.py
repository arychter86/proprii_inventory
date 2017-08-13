from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from inventory.validators import *


class Inventory(models.Model):
    author = models.ForeignKey('auth.User',null=True)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=10, blank=True, validators=[numeric])
    created_date = models.DateTimeField(default=timezone.now)
    client_name = models.CharField(max_length=200, blank=True)
    notes = models.TextField(max_length=1000,blank=True)
    def __str__(self):
        return str(self.id) + "_" +self.name + ", klient: " + self.client_name + ", data: " + str(self.created_date)

class InventoryForm(forms.ModelForm):

    class Meta:
        model = Inventory
        fields = [ 'name', 'city', 'street', 'code', 'created_date', 'client_name','notes']
        widgets = {
            'code': forms.TextInput(attrs={'type':'number'}),
        }

class InventoryMap(models.Model):
    UPLOAD_TO = 'photos/maps/'
    inventory = models.ForeignKey('Inventory', related_name='maps')
    picture = models.ImageField(upload_to = UPLOAD_TO, default = 'no-map.jpg')
    created_date = models.DateTimeField(default=timezone.now)
    @receiver(pre_delete)
    def delete_repo(sender, instance, **kwargs):
        if sender == InventoryMap:
            instance.picture.delete(save=True)

class InventoryMapForm(forms.ModelForm):
    class Meta:
        model = InventoryMap
        fields = ['picture']



class Tree(models.Model):
    inventory = models.ForeignKey('Inventory', related_name='trees')
    tree_number = models.IntegerField(default=0,validators=[validate_tree_number])
    name = models.CharField(max_length=200)
    latin_name = models.CharField(max_length=200, blank=True)
    height_m = models.IntegerField(blank=True, null=True, validators=[validate_postive_int])
    crown_area = models.IntegerField(blank=True, null=True,  validators=[validate_postive_int])
    M_CHOICES = [("m", "m"),("m2","m2")]

    crown_area_unit = models.CharField(max_length=2, choices=M_CHOICES, default='1')

    notes = models.TextField(max_length=1000, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id) + ": " + self.name



class TreeForm(forms.ModelForm):
    class Meta:
        model = Tree
        fields = ['tree_number','name', 'latin_name', 'height_m', 'crown_area', 'crown_area_unit', 'notes']
        labels = {
            'name': _('Name'),
        }
        help_texts = {
            'name': _('Choose polish name.'),
        }
        widgets = {
            'notes': forms.Textarea(attrs={'width':'100%','cols': 10, 'rows': 3}),
        }

class TreeFormSmall(forms.ModelForm):
    class Meta:
        model = Tree
        fields = ['tree_number','name', 'latin_name']

class TreeOnMap(models.Model):
    inventorymap = models.ForeignKey('InventoryMap', related_name = 'treesonmap')
    tree = models.ForeignKey('Tree')
    x_pos = models.IntegerField(default=0, validators=[validate_postive_int])
    y_pos = models.IntegerField(default=0, validators=[validate_postive_int])
    radius = models.IntegerField(default=10, validators=[validate_postive_int])

class TreeOnMapForm(forms.ModelForm):
    class Meta:
        model = TreeOnMap
        fields = ['x_pos', 'y_pos', 'radius', 'tree']

class TreeImage(models.Model):
    UPLOAD_TO = 'photos/trees/'
    tree = models.ForeignKey('Tree',null=True, related_name='images')
    picture = models.ImageField(upload_to = UPLOAD_TO, default = 'no-img.jpg')
    created_date = models.DateTimeField(default=timezone.now)
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
        fields = []


class TreeTrunk(models.Model):
    tree = models.ForeignKey('Tree',related_name='trunks')
    trunk_cm = models.IntegerField(validators=[validate_trunk])
    meas_height_cm = models.IntegerField( default='130',validators=[validate_postive_int])
    created_date = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return str(self.id) + "_" + + str(self.trunk_cm) + "__" + str(self.created_date)

class TreeTrunkForm(forms.ModelForm):

    class Meta:
        model = TreeTrunk
        fields = ['trunk_cm', 'meas_height_cm']
