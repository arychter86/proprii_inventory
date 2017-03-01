from django.shortcuts import render

# Create your views here.
def inv_list(request):
    return render(request, 'inventory/inv_list.html', {})
