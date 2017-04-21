from django.shortcuts import render
from .models import Inventory, InventoryForm, Tree, TreeForm
from django.forms import modelformset_factory

# Create your views here.
def inv_list(request):
    inventorys = Inventory.objects.all()
    return render(request, 'inventory/inv_list.html', {'inventorys':inventorys})


def inventory(request,id):

    username = None
    if request.user.is_authenticated():
        username = request.user.username

    try:
        inv_obj = Inventory.objects.get(id=id)
    except Inventory.DoesNotExist:
        inv_obj = Inventory()

    if request.method == 'POST':

        if inv_obj != None:
            form = InventoryForm(request.POST, request.FILES, instance=inv_obj)
        else:
            form = InventoryForm(request.POST, request.FILES)
            print(form.instance.id)
            id = form.instance.id

        if 'trees' in request.POST:
            TreeFormSet = modelformset_factory(Tree,TreeForm,extra=2)
            formset = TreeFormSet(request.POST, request.FILES)
            print('Formset Saved')
            if formset.is_valid():
                formset.save()

        elif 'inventory' in request.POST:
            if form.is_valid():
                form.save()
                # do something.\
                id = form.instance.id
                print('Inventory Data Saved')
            else:
                print('Problem with saving', form.errors)


    try:
        form = InventoryForm(instance=inv_obj)
        TreeFormSet = modelformset_factory(Tree, TreeForm,extra=2)
        formset = TreeFormSet(queryset=Tree.objects.filter(inventory = inv_obj ))
    except Inventory.DoesNotExist:
        form =  InventoryForm()


    form = form.as_ul()

    return render(request, 'inventory/inventory.html', {'form': form,'formset':formset,'id':id})
