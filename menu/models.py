from django.db import models
from django.utils import timezone

class Menu(models.Model):
    season = models.CharField(max_length=20)
    items = models.ManyToManyField('Item', related_name='items')
    created_date = models.DateTimeField(
            default=timezone.now)
    expiration_date = models.DateTimeField(
            blank=True, null=True)

    def __str__(self):
        return self.season

    # this is for the admin only. 
    def number_of_items(self):
        ''' uses our templatetag filter function to be used in the 
        admin.py file under the MenuAdmin for 'list_display=[]'''
        from menu.templatetags.menu_extras import item_count 
        return "{} items in menu".format(item_count(self.items))

class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    chef = models.ForeignKey('auth.User')
    created_date = models.DateTimeField(
            default=timezone.now)
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
