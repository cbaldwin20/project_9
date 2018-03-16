from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.utils import timezone
from operator import attrgetter
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from .models import Menu, Item, Ingredient
from .forms import MenuForm, ItemForm 

def menu_list(request):
    current_time = timezone.now()
    #*********change 'lte' to 'gte'
    menus = Menu.objects.filter(expiration_date__lte=current_time).order_by('expiration_date')
    return render(request, 'menu/list_all_current_menus.html', {'menus': menus})

def menu_detail(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'menu/detail_item.html', {'item': item})

def create_new_menu(request):
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save()
            #**************I may have messed up the 'pk=form.pk'
            return redirect('menu/menu_detail.html', {'menu': menu})
    else:
        form = MenuForm()
    return render(request, 'menu/new_menu.html', {'form': form})

def edit_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    items = Item.objects.all()
    if request.method == "POST":
        menu.season = request.POST.get('season', '')
        #*********possibly change this 'expiration_date' part. 
        menu.expiration_date = datetime.strptime(request.POST.get('expiration_date', ''), '%m/%d/%Y')
        menu.items = request.POST.get('items', '')
        menu.save()
        return redirect('menu/menu_detail.html', {'menu': menu})

    return render(request, 'menu/edit_menu.html', {
        'menu': menu,
        'items': items,
        })

def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    form = ItemForm(instance=item)
    if request.method == "POST":
        form = ItemForm(instance=item, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu/detail_item.html', {'item': item})
    return render(request, 'menu/item_edit.html', {'form': form})


 


