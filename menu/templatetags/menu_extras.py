#****this templatetags file is only for the admin. 
from django import template 

register = template.Library()

@register.filter('time_estimate')
def item_count(count):
	'''Tells how many items are in a Menu object'''
	#what 'count' is is 'Menu.items' which is a 
	#many to many field, so you have to do '.all()'
	# on it first before you can do 'len()'. 
	total1 = count.all()
	total = len(total1)
	return total 