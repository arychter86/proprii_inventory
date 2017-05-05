from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from .models import Inventory, InventoryForm, Tree, TreeForm, TreeImage, TreeImageForm
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
# Create your views here.

@login_required(login_url='/login/')
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
                    print(instance)
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


class TreeView(View):
    template_name = "inventory/tree.html"
    username = None


    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            username = request.user.username
        TreeImageFormSet = modelformset_factory(TreeImage, TreeImageForm, extra=0, can_delete=True)
        if 'id' in kwargs:
            id = kwargs.get('id')
        if 'id_t' in kwargs:
            id_t = kwargs.get('id_t')
            tree_obj=Tree.objects.filter(id=id_t)
            if tree_obj.count() > 0:
                tree_obj = Tree.objects.get(id=id_t)
                #retrieve images for tree_obj
                t_imgs = TreeImage.objects.filter(tree = tree_obj)
            else:
                tree_obj = Tree()
                #set inventory, there are no trees yet
                setattr(tree_obj, 'inventory', Inventory.objects.get(id=id))
        else:
            id_t = 0;
            tree_obj = Tree()
            setattr(tree_obj, 'inventory', Inventory.objects.get(id=id))

        form = TreeForm(instance=tree_obj)
        formset = TreeImageFormSet(queryset=t_imgs)
        return render(request, self.template_name, {'form': form,'formset':formset,'id':id,'id_t':id_t})

    def post(self, request, *args, **kwargs):
        id = kwargs.get('id')

        if 'id_t' in kwargs:
            id_t = kwargs.get('id_t')
            if id_t != '0':
                tree_obj = Tree.objects.get(id=id_t)
                form = TreeForm(request.POST, request.FILES,instance=tree_obj)
            else:
                form = TreeForm(request.POST, request.FILES)
        else:
            form = TreeForm(request.POST, request.FILES)

        setattr(form.instance, 'inventory', Inventory.objects.get(id=id))

        if 'delete' in request.POST:
            tree_obj.delete()
            return HttpResponseRedirect('/inventory/'+id)

        if form.is_valid():
            # <process form cleaned data>
            instance = form.save(commit=False)
            instance.inventory =  Inventory.objects.get(id=id)
            instance.save()
            print("Tree saved",instance)
            form = TreeForm(instance=instance)
        return HttpResponseRedirect('/inventory/'+id+'/tree/'+str(instance.id)+'/')
