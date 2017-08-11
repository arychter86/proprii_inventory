from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import *
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse, Http404
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
            if id != '0':
                id = kwargs.get('id')
                queryset = Inventory.objects.filter(author=user)
                inv_obj = get_object_or_404(queryset, pk=id)
            else:
                inv_obj = Inventory()
                setattr(inv_obj, 'author', user)

            trees = Tree.objects.filter(inventory = inv_obj )
            try:
                form = InventoryForm(instance=inv_obj)
            except Inventory.DoesNotExist:
                form =  InventoryForm()

            return render(request, 'inventory/inventory.html', {'id':id,'form': form,'trees':trees})
        else:
            raise Http404("Missing inventory id.")


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

            if 'inventory' in request.POST:
                if form.is_valid():
                    inv_obj = form.save(commit=False)
                    # set the author
                    inv_obj.author = request.user
                    inv_obj.save()
                    new_id = inv_obj.id
                    print('Inventory Data Saved',form.instance)
                    return HttpResponseRedirect('/inventory/'+str(new_id)+'/')
                else:
                    print('Problem with saving', form.errors)
            elif 'delete' in request.POST:
                inv_obj.delete()
                return HttpResponseRedirect('/')

            inv_obj = Inventory.objects.filter(id = id )
            trees = Tree.objects.filter(inventory = inv_obj )
            return render(request, 'inventory/inventory.html', {'id':id,'form': form,'trees':trees})
        else:
            raise Http404("Missing inventory id.")


class TreeTrunkDeleteView(View):
    username = None
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            username = request.user.username
        print('Tree Trunk deleted')
        if 'id_t' in kwargs and 'id' in kwargs and 'id_tt' in kwargs:
            id = kwargs.get('id')
            id_t = kwargs.get('id_t')
            id_tt = kwargs.get('id_tt')
            inv_obj = get_object_or_404(Inventory, pk=id)
            queryset = Tree.objects.filter(inventory=inv_obj)
            tree_obj = get_object_or_404(queryset, pk=id_t)
            queryset = TreeTrunk.objects.filter(tree=tree_obj)
            trunk = get_object_or_404(queryset, pk=id_tt)

            trunk.delete()
            print('Tree Trunk deleted')
        return HttpResponseRedirect('/inventory/'+str(id)+'/tree/'+str(tree_obj.id)+'/')

class TreeDeleteView(View):
    template_name = "inventory/tree.html"
    username = None

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            username = request.user.username

        if 'id_t' in kwargs and 'id' in kwargs:
            id = kwargs.get('id')
            id_t = kwargs.get('id_t')
            inv_obj = get_object_or_404(Inventory, pk=id)
            queryset = Tree.objects.filter(inventory=inv_obj)
            tree_obj = get_object_or_404(queryset, pk=id_t)
            tree_obj.delete()
            print('Tree deleted')
        return HttpResponseRedirect('/inventory/'+str(id))

class TreeImageDeleteView(View):
    template_name = "inventory/tree.html"
    username = None

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            username = request.user.username

        if 'id_image' in kwargs and 'id_t' in kwargs and 'id' in kwargs:
            id = kwargs.get('id')
            id_t = kwargs.get('id_t')
            id_image = kwargs.get('id_image')
            inv_obj = get_object_or_404(Inventory, pk=id)
            queryset = Tree.objects.filter(inventory=inv_obj)
            tree_obj = get_object_or_404(queryset, pk=id_t)
            queryset = TreeImage.objects.filter(tree=tree_obj)
            image = get_object_or_404(queryset, pk=id_image)
            image.delete()
            print('Tree deleted')
        return HttpResponseRedirect('/inventory/'+str(id)+'/tree/'+str(id_t)+'/')

class TreeView(View):
    template_name = "inventory/tree.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            username = request.user.username

        if 'id_t' in kwargs and 'id' in kwargs:
            id = kwargs.get('id')
            id_t = kwargs.get('id_t')

            inv_obj = get_object_or_404(Inventory, pk=id)

            if id_t != '0':
                queryset = Tree.objects.filter(inventory=inv_obj)
                tree_obj = get_object_or_404(queryset, pk=id_t)
            else:
                tree_obj = Tree()
                # set the initial tree id/ should be done in Tree model?
                if Tree.objects.all().filter(inventory=inv_obj).order_by('-tree_number'):
                    top = Tree.objects.all().filter(inventory=inv_obj).order_by('-tree_number')[0]
                    tree_obj.tree_number = top.tree_number + 1
                else:
                    tree_obj.tree_number = 1

            setattr(tree_obj, 'inventory', Inventory.objects.get(id=id))
        else:
            raise Http404("Missing inventory or tree id.")
        # tree form
        form = TreeForm(instance=tree_obj)
        #List of images
        image_list = TreeImage.objects.filter(tree = tree_obj)
        #List of trunks
        trunk_list = TreeTrunk.objects.filter(tree = tree_obj)
        # new trunk form
        trunk_form = TreeTrunkForm()
        return render(request, self.template_name, {'trunk_form':trunk_form,'trunk_list':trunk_list,'form': form,'image_list':image_list,'inventory':inv_obj,'id':id,'id_t':id_t})

    def post(self, request, *args, **kwargs):

        if 'id_t' in kwargs and 'id' in kwargs:
            id = kwargs.get('id')
            id_t = kwargs.get('id_t')

            # There must be the Iventory!
            inv_obj = get_object_or_404(Inventory, pk=id)
            # create empty tree object
            tree_obj = Tree()
            # handle tree form
            if 'save_tree' in request.POST or 'save_and_exit' in request.POST :
                # get the tree form
                if Tree.objects.filter(pk=id_t).exists():
                    queryset = Tree.objects.filter(inventory=inv_obj)
                    tree_obj = get_object_or_404(queryset, pk=id_t)
                    form = TreeForm(request.POST, request.FILES,instance=tree_obj)
                    tree_obj = form.instance
                else:   # this is a new Tree!
                    print('Adding new TREE for INVENTORY:',inv_obj)
                    form = TreeForm(request.POST, request.FILES)
                    setattr(form.instance, 'inventory', inv_obj)

                #validatin data form a form
                if form.is_valid():
                    # <process form cleaned data>
                    tree_obj = form.save(commit=False)
                    tree_obj.inventory =  Inventory.objects.get(id=id)
                    tree_obj.save()
                    id_t = str(tree_obj.id)
                    print("TREE saved:",tree_obj)
                    if 'save_and_exit' in request.POST :
                        return HttpResponseRedirect('/inventory/'+id+'/')
                    elif 'save_and_new' in request.POST :
                        return HttpResponseRedirect('/inventory/'+id+'/tree/0/')  
                    else:
                        return HttpResponseRedirect('/inventory/'+id+'/tree/'+id_t+'/')

                else:
                    print('Tree form not valid ', form.errors)


            if 'add_trunk' in request.POST and id_t != '0':
                trunk_form = TreeTrunkForm(request.POST, request.FILES)
                queryset = Tree.objects.filter(inventory=inv_obj)
                tree_obj = get_object_or_404(queryset, pk=id_t)
                # tree form
                form = TreeForm(instance=tree_obj)
                if trunk_form.is_valid():
                    # <process form cleaned data>
                    trunk = trunk_form.save(commit=False)
                    trunk.tree =  tree_obj
                    trunk.save()
                    trunk_form = TreeTrunkForm()
                    print('Adding new trunk size ', str(trunk.trunk_cm))
                else:
                    print('Trunk form not valid ', trunk_form.errors)
            else:
                # new trunk form
                trunk_form = TreeTrunkForm()

        #List of images
        image_list = TreeImage.objects.filter(tree = tree_obj)
        #List of trunks
        trunk_list = TreeTrunk.objects.filter(tree = tree_obj)

        return render(request, self.template_name, {'trunk_form':trunk_form,'trunk_list':trunk_list,'form': form,'image_list':image_list,'inventory':inv_obj,'id':id,'id_t':id_t})


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
