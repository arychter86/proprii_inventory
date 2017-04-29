from django.contrib import admin
from .models import Inventory, Tree, TreeImage
# Register your models here.

admin.site.register(Inventory)
admin.site.register(Tree)
admin.site.register(TreeImage)
