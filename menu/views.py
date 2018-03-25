from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.utils import timezone
from operator import attrgetter
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from .models import Menu, Item, Ingredient
from .forms import MenuForm, ItemForm 

def menu_list(request):
    """is the home page"""
    current_time = timezone.now()
    #*********change 'lte' to 'gte'
    menus = Menu.objects.filter(expiration_date__gte=current_time).order_by(
        'expiration_date')
    return render(request, 'menu/list_all_current_menus.html', {'menus': menus})

def menu_detail(request, pk):
    """give the detail of a certain menu"""
    menu = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})

def item_detail(request, pk):
    """detail of a specific item"""
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'menu/detail_item.html', {'item': item})

def create_new_menu(request):
    """create new menu"""
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save()
            return redirect('mysite:menu_detail', pk=menu.pk)
    
    form = MenuForm()
    return render(request, 'menu/new_menu.html', {'form': form})

def edit_menu(request, pk):
    """edit a menu"""
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        form = MenuForm(instance=menu, data=request.POST)
        if form.is_valid:
            form.save()
            
            return redirect('mysite:menu_detail', pk=pk)
    form = MenuForm(instance=menu)
    return render(request, 'menu/edit_menu.html', {'form': form})

def edit_item(request, pk):
    """edit an item"""
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = ItemForm(instance=item, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('mysite:item_detail', pk=pk)
    form = ItemForm(instance=item)
    return render(request, 'menu/item_edit.html', {'form': form})




 


