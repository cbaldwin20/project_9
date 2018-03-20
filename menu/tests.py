from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from menu.models import Menu, Item, Ingredient 
from menu.forms import MenuForm 

user = User.objects.get(id=1)
class MyTests(TestCase):

    def setUp(self):
        self.ingredient = Ingredient.objects.create(
            name="lskdjflkjfd"
            )
        self.item = Item(
                name="LKJklsjd",
            description="LKSJdlfkjsldfjsd",
            chef=user,
            )
        self.item.save()
        self.item.ingredients.add(self.ingredient)
        
        self.menu = Menu(
            season="asdfasdfadsfadsf",
            expiration_date=timezone.now() + timezone.timedelta(days=1)
            )
        self.menu.save()
        self.menu.items.add(self.item)

    def test_models_creation(self):
        now = timezone.now()
        self.assertLess(self.item.created_date, now)
        self.assertLess(self.menu.created_date, now)
        self.assertIn(self.ingredient, self.item.ingredients.all())
        self.assertIn(self.item, self.menu.items.all())
        self.assertEqual(user, self.item.chef)

    def test_menu_list_view(self):
        resp = self.client.get(reverse('mysite:menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.menu, resp.context['menus'])
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')
        self.assertContains(resp, self.menu.season)

    def test_menu_detail_view(self):
        resp = self.client.get(reverse('mysite:menu_detail', kwargs={'pk': self.menu.id }))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.menu, resp.context['menu'])
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')
        self.assertContains(resp, self.menu.season)

    def test_item_detail_view(self):
        resp = self.client.get(reverse('mysite:item_detail', kwargs={'pk': self.item.id }))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.item, resp.context['item'])
        self.assertTemplateUsed(resp, 'menu/detail_item.html')
        self.assertContains(resp, self.item.name)


    def test_menuform_valid(self):
        form = MenuForm(data={
                        'expiration_date': timezone.now() + timezone.timedelta(days=2),
                        'season': 'Spring 2018',
                        'created_date': timezone.now(),
                        'items': ['1']
                             })
        self.assertTrue(form.is_valid())



    def test_create_new_menu_view(self):
        resp = self.client.get(reverse('mysite:menu_new'))
        self.assertEqual(resp.status_code, 200)
        form = MenuForm() 
        self.assertEqual(form, resp.context['form'])
        self.assertTemplateUsed(resp, 'menu/new_menu.html')
        self.assertContains(resp, "Create new menu")






