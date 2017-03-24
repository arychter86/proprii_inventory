from django.shortcuts import render
from .models import Inventory

# Create your views here.
def inv_list(request):
    inventorys = Inventory.objects.all()
    return render(request, 'inventory/inv_list.html', {'inventorys':inventorys})


def inventory(request,id):
    try:
        inventory = Inventory.objects.get(id=id)
    except Inventory.DoesNotExist:
        inventory = None
    return render(request, 'inventory/inventory.html', {'inventory':inventory})
