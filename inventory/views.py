from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Inventory, InventoryForm, Tree, TreeForm, TreeImage, TreeImageForm
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
# Create your views here.

class InventoryList(View):
    template_name = "inventory/inv_list.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            user = request.user
        inventorys = Inventory.objects.filter(author=user)
        return render(request, 'inventory/inv_list.html', {'inventorys':inventorys})

class InventoryView(View):
    template_name = "inventory/inventory.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            user = request.user

        if 'id' in kwargs:
            id = kwargs.get('id')
            queryset = Inventory.objects.filter(author=user)
            inv_obj = get_object_or_404(queryset, pk=id)
        else:
            inv_obj = Inventory()
            setattr(inv_obj, 'author', user)
            id = 0

        TreeFormSet = modelformset_factory(Tree, TreeForm,extra=0, can_delete=True)
        formset = TreeFormSet(queryset=Tree.objects.filter(inventory = inv_obj ))
        try:
            form = InventoryForm(instance=inv_obj)
        except Inventory.DoesNotExist:
            form =  InventoryForm()

        return render(request, 'inventory/inventory.html', {'form': form,'formset':formset,'id':id})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            user = request.user
        if 'id' in kwargs:
            id = kwargs.get('id')
            if id != '0':
                queryset = Inventory.objects.filter(author=user)
                inv_obj = get_object_or_404(queryset, pk=id)
                form = InventoryForm(request.POST, request.FILES, instance=inv_obj)
            else:
                form = InventoryForm(request.POST, request.FILES)

        if 'trees' in request.POST:
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
                inv_obj = form.instance
                print('Inventory Data Saved',form.instance)
            else:

                print('Problem with saving', form.errors)

        try:
            form = InventoryForm(instance=inv_obj)
            TreeFormSet = modelformset_factory(Tree, TreeForm, extra=0, can_delete=True)
            formset = TreeFormSet(queryset=Tree.objects.filter(inventory = inv_obj ))
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

        if 'id_t' in kwargs and 'id' in kwargs:
            id = kwargs.get('id')
            id_t = kwargs.get('id_t')
            inv_obj = get_object_or_404(Inventory, pk=id)

            queryset = Tree.objects.filter(inventory=inv_obj)
            tree_obj = get_object_or_404(queryset, pk=id_t)

            t_imgs = TreeImage.objects.filter(tree = tree_obj)

        elif 'id' in kwargs:
            id = kwargs.get('id')
            inv_obj = get_object_or_404(Inventory, pk=id)
            id_t = 0;
            tree_obj = Tree()
            setattr(tree_obj, 'inventory', Inventory.objects.get(id=id))
        else:
            raise Http404("Missing inventory id.")

        form = TreeForm(instance=tree_obj)
        if 't_imgs' in locals():
            formset = TreeImageFormSet(queryset=t_imgs)
        else:
            formset = TreeImageFormSet(queryset=TreeImage.objects.none())
            print('Test')

        return render(request, self.template_name, {'form': form,'formset':formset,'inventory':inv_obj,'id':id,'id_t':id_t})

    def post(self, request, *args, **kwargs):
        id = kwargs.get('id')

        if 'id_t' in kwargs and 'id' in kwargs:
            id = kwargs.get('id')
            id_t = kwargs.get('id_t')
            inv_obj = get_object_or_404(Inventory, pk=id)
            if id_t != '0':
                queryset = Tree.objects.filter(inventory=inv_obj)
                tree_obj = get_object_or_404(queryset, pk=id_t)
                form = TreeForm(request.POST, request.FILES,instance=tree_obj)
            else:
                print('Adding new TREE for INVENTORY:',inv_obj)
                form = TreeForm(request.POST, request.FILES)
                setattr(form.instance, 'inventory', inv_obj)

            if form.is_valid():
                # <process form cleaned data>
                tree_obj = form.save(commit=False)
                tree_obj.inventory =  Inventory.objects.get(id=id)
                tree_obj.save()
            else:
                raise Http404("Tree formset not valid.")

            t_imgs = TreeImage.objects.filter(tree = tree_obj)

            if 'delete' in request.POST:
                tree_obj.delete()
                return HttpResponseRedirect('/inventory/'+id)


            print("INVENTORY:",inv_obj,"TREE saved:",tree_obj)
            form = TreeForm(instance=tree_obj)

        return HttpResponseRedirect('/inventory/'+id+'/tree/'+str(tree_obj.id)+'/')
