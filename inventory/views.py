from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Inventory, InventoryForm, Tree, TreeForm, TreeImage, TreeImageForm, TreeTrunk, TreeTrunkForm
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.core.files import File
import json
import base64
from django.conf import settings
import os.path
# Create your views here.

class InventoryList(View):
    template_name = "inventory/inv_list.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            user = request.user
        inventorys = Inventory.objects.filter(author=user)

        for inv in inventorys:
            inv.treenum = Tree.objects.filter(inventory=inv).count()
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

                inv_obj = form.save(commit=False)
                # set the author
                inv_obj.author = request.user
                inv_obj.save()

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
        TreeImageFormSet = modelformset_factory(TreeImage, TreeImageForm, extra=0, can_delete=True)

        form = TreeForm(instance=tree_obj)
        if 't_imgs' in locals():
            formset = TreeImageFormSet(queryset=t_imgs)
        else:
            formset = TreeImageFormSet(queryset=TreeImage.objects.none())
            print('Test')

        image_form = TreeImageForm()
        trunk_form = TreeTrunkForm()
        return render(request, self.template_name, {'trunk_form':trunk_form,'image_form': image_form, 'form': form,'formset':formset,'inventory':inv_obj,'id':id,'id_t':id_t})

    def post(self, request, *args, **kwargs):

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
                print('FORM:',form)
                setattr(form.instance, 'inventory', inv_obj)

            if 'tree' in request.POST:
                if form.is_valid():
                    # <process form cleaned data>
                    tree_obj = form.save(commit=False)
                    tree_obj.inventory =  Inventory.objects.get(id=id)
                    tree_obj.save()
                    print("INVENTORY:",inv_obj,"TREE saved:",tree_obj)
                else:
                    raise Http404("Tree formset not valid.")

                t_imgs = TreeImage.objects.filter(tree = tree_obj)

            elif 'delete_imgs' in request.POST:
                TreeImageFormSet = modelformset_factory(TreeImage, TreeImageForm, extra=0, can_delete=True)

                formset = TreeImageFormSet(request.POST)
                if formset.is_valid():
                    instances = formset.save(commit=False)
                    for instance in formset.deleted_objects:
                        instance.delete()
                return HttpResponseRedirect('/inventory/'+id+'/tree/'+str(tree_obj.id)+'/')
            elif 'add_img' in request.POST:
                image_form = TreeImageForm(request.POST, request.FILES)
                print(image_form)
                if image_form.is_valid():
                    # <process form cleaned data>
                    img = image_form.save(commit=False)
                    img.picture = image_form.cleaned_data['picture']
                    img.tree =  Tree.objects.get(id=id_t)
                    img.save()
                else:
                    raise Http404("Tree formset not valid.")

        return HttpResponseRedirect('/inventory/'+id+'/tree/'+str(tree_obj.id)+'/')

class TreeImageView(View):
    template_name = "inventory/tree_image.html"


    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            user = request.user

        if 'id_t' in kwargs and 'id' in kwargs:
            id = kwargs.get('id')
            id_t = kwargs.get('id_t')
            queryset = Inventory.objects.filter(author=user)
            inv_obj = get_object_or_404(queryset, pk=id)

            queryset = Tree.objects.filter(inventory=inv_obj)
            tree_obj = get_object_or_404(queryset, pk=id_t)
        else:
            raise Http404("Missing inventory or tree id.")

        return render(request, self.template_name, {'tree':tree_obj,'inventory':inv_obj,'id':id,'id_t':id_t})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            user = request.user
        if 'id_t' in kwargs and 'id' in kwargs:
            id = kwargs.get('id')
            id_t = kwargs.get('id_t')

            queryset = Inventory.objects.filter(author=user)
            inv_obj = get_object_or_404(queryset, pk=id)

            queryset = Tree.objects.filter(inventory=inv_obj)
            tree_obj = get_object_or_404(queryset, pk=id_t)

        else:
            raise Http404("Missing inventory or tree id.")

        json_data = json.loads(request.body) # request.raw_post_data w/ Django < 1.4
        if 'id' in json_data and 'id_t' in json_data and 'img_base64' in json_data:

            print('Image data for inv ', json_data['id'],' and tree ',json_data['id_t'])
            try:
                data_url = json_data['img_base64']
            except KeyError:
              HttpResponseServerError("Malformed data!")

            content = data_url.split(';')[1]
            image_encoded = content.split(',')[1]
            image_binary = base64.decodebytes(image_encoded.encode('utf-8'))

            # create new image in DB
            t_img = TreeImage()
            t_img.author = user
            t_img.tree = tree_obj
            t_img.description = 'img'
            t_img.save(force_insert=True)
            filename = 'tree_'+str(tree_obj.id)+'_image_'+str(t_img.id)+'.jpeg'
            full_filename = os.path.join(settings.MEDIA_ROOT, "photos", filename)
            print('Saving image to', full_filename)
            with open(full_filename,'wb') as f:
                f.write(image_binary)
            t_img.picture.name = "photos/"+filename
            t_img.save()
        #return HttpResponseRedirect('/inventory/'+id+'/tree/'+str(tree_obj.id)+'/')
        redirect = '/inventory/'+id+'/tree/'+str(tree_obj.id)+'/';
        response_data = {}
        response_data['redirect'] =redirect
        response_data['id'] = id
        response_data['id'] = id_t
        data = json.dumps(response_data)
        return HttpResponse(data, content_type='application/json')
