from django.shortcuts import render
from .models import Inventory, InventoryForm
from django.forms import modelformset_factory

# Create your views here.
def inv_list(request):
    inventorys = Inventory.objects.all()
    return render(request, 'inventory/inv_list.html', {'inventorys':inventorys})


def inventory(request,id):

    if id:
        inventory = Inventory.objects.get(id=id)
    else:
        inventory = None

    if request.method == 'POST':
        form = InventoryForm(request.POST, request.FILES, instance=inventory)
        if form.is_valid():
            form.save()
            # do something.
            return inv_list(request)
    else:
        try:
            inventory = Inventory.objects.get(id=id)
            form = InventoryForm(instance=inventory)
        except Inventory.DoesNotExist:
            inventory = None
            form =  InventoryForm()


    return render(request, 'inventory/inventory.html', {'form': form})
