from django.shortcuts import render
from .models import Inventory, InventoryForm
from django.forms import modelformset_factory

# Create your views here.
def inv_list(request):
    inventorys = Inventory.objects.all()
    return render(request, 'inventory/inv_list.html', {'inventorys':inventorys})


def inventory(request,id):

    try:
        inv_obj = Inventory.objects.get(id=id)
    except Inventory.DoesNotExist:
        inv_obj = Inventory()

    try:
        form = InventoryForm(instance=inv_obj)
    except Inventory.DoesNotExist:
        form =  InventoryForm()

    if request.method == 'POST':
        if inv_obj != None:
            form = InventoryForm(request.POST, request.FILES, instance=inv_obj)
        else:
            form = InventoryForm(request.POST, request.FILES)
            print(form.instance.id)
            id = form.instance.id

        if form.is_valid():
            form.save()
            # do something.\
            id = form.instance.id
            print('Saved')
        else:
            print('Problem with saving', form.errors)


    form = form.as_ul()

    return render(request, 'inventory/inventory.html', {'form': form,'id':id})
