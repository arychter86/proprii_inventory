from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Inventory, InventoryForm, Tree, TreeForm
from django.forms import modelformset_factory

# Create your views here.
def inv_list(request):
    inventorys = Inventory.objects.all()
    return render(request, 'inventory/inv_list.html', {'inventorys':inventorys})

@login_required(login_url='/login/')
def inventory(request,id):

    username = None
    if request.user.is_authenticated():
        username = request.user.username

    try:
        inv_obj = Inventory.objects.get(id=id)
    except Inventory.DoesNotExist:
        inv_obj = Inventory()

    TreeFormSet = modelformset_factory(Tree, TreeForm,extra=0, can_delete=True)
    formset = TreeFormSet(queryset=Tree.objects.filter(inventory = inv_obj ))

    if request.method == 'POST':

        if inv_obj != None:
            form = InventoryForm(request.POST, request.FILES, instance=inv_obj)
        else:
            form = InventoryForm(request.POST, request.FILES)
            print(form.instance.id)
            id = form.instance.id

        if 'trees' in request.POST:
            TreeFormSet = modelformset_factory(Tree, TreeForm, extra=0, can_delete=True)
            formset = TreeFormSet(request.POST, request.FILES)
            print(request.POST)
            if formset.is_valid():
                instances = formset.save(commit=False)
                for instance in formset.deleted_objects:
                    instance.delete()
                for instance in instances:
                    instance.inventory = form.instance
                    instance.save()
                formset = TreeFormSet(queryset=Tree.objects.filter(inventory = inv_obj ))
                print('Formset Saved')
            else:
                print('Formset invalid, not saved!',formset.errors)

        elif 'inventory' in request.POST:
            if form.is_valid():
                form.save()
                # do something
                id = form.instance.id
                print('Inventory Data Saved')
            else:
                print('Problem with saving', form.errors)

    try:
        form = InventoryForm(instance=inv_obj)

    except Inventory.DoesNotExist:
        form =  InventoryForm()

    return render(request, 'inventory/inventory.html', {'form': form,'formset':formset,'id':id})
