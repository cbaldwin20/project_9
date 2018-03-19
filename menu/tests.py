from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from menu.models import Menu, Item, Ingredient 

user = User.objects.get(id=1)
class MenuModelTests(TestCase):
    def test_course_creation(self):
        
        ingredient = Ingredient.objects.create(
            name="lskdjflkjfd"
            )
        item = Item(
                name="LKJklsjd",
            description="LKSJdlfkjsldfjsd",
            chef=user,
            )
        item.save()
        item.ingredients.add(ingredient)
        
        menu = Menu(
            season="asdfasdfadsfadsf",
            )
        menu.save()
        menu.items.add(item)

        now = timezone.now()
        self.assertLess(item.created_date, now)
        self.assertLess(menu.created_date, now)



