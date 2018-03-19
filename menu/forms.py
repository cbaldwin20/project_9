from django import forms
#from django.forms.extras.widgets import SelectDateWidget

from .models import Menu, Item, Ingredient

class MenuForm(forms.ModelForm):
    expiration_date = forms.DateField(widget=forms.SelectDateWidget())
    
    class Meta:
        model = Menu
        exclude = ('created_date',) 

class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        exclude = ('created_date',) 
 