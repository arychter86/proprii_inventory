from django import forms
from django import User

class InventoryForm(forms.Form):
    author = forms.ModelChoiceField(queryset=User.objects.all())
    name = forms.CharField(max_length=200)
    city = forms.CharField(max_length=100)
    street = forms.CharField(max_length=100)
    code = forms.CharField(max_length=10)
    created_date = forms.DateTimeField()
    client_name = forms.CharField(max_length=200)
