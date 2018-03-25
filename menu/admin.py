from django.contrib import admin
from .models import Menu, Item, Ingredient
from datetime import date

#this 'YearListFilter' is a custom filter that we 
# put in the MenuAdmin 'list_filter' below. 
# it makes it so if you click on '2018' it will return
# all the instances created in 2018, etc. 
class YearListFilter(admin.SimpleListFilter):
	"""can filter menu instance by year"""
	title = 'year created'

	parameter_name = 'year'

	def lookups(self, request, model_admin):
		return (
			#the value '2017' '2018' on the left is what goes in the url
			('2017', '2017'),
			('2018', '2018'),
			)
	def queryset(self, request, queryset):
		if self.value() == '2017':
			return queryset.filter(created_date__gte=date(2017, 1, 1),
									created_date__lte=date(2017, 12, 31))
		# could probably keep this code dry by just doing
		# if self.value():
		# 	return queryset.filter(created_date__gte=date(self.value(), 1, 1))
		#   return queryset.filter(created_date__gte=date(self.value(), 12, 31))

		if self.value() == '2018':
			return queryset.filter(created_date__gte=date(2018, 1, 1),
									created_date__lte=date(2018, 12, 31))

class ItemAdmin(admin.ModelAdmin):
	#'fields' will put what order the fields are presented in the 
	# detail page. 
	fields = ['name', 'ingredients', 'description',
	 'chef', 'created_date', 'standard']

	search_fields = ['name']

	# 'radio_fields' changes the 'chef' from a dropdown to a 
	# radio button selection. 
	radio_fields = {'chef': admin.HORIZONTAL}

class MenuAdmin(admin.ModelAdmin):
	# this will put a search bar in the list
	# of menus page. 'season' means whatever we
	# search, only scan the season attribute of 
	# each model instance. 
	search_fields = ['season']
	# for the list page, will add a filter tab on
	# the side to click on. For this datetimefield it will give 
	# 'today', 'last 7 days' etc. 
	list_filter = ['created_date', YearListFilter]

	# this shows what fields will be shown in the list menu. 
	# the 'number_of_items' is a method in our 'models.py' file under
	# the class Menu() model. 
	list_display = ['season', 'expiration_date', 'number_of_items']

	#this makes it so we can edit something in the list page instead of
	# having to click into the detail page. Not super necessary but 
	# makes things a bit quicker I guess. Note- must already be in the 
	# 'list_display' to be in the 'list_editable'. 
	list_editable = ['expiration_date']

	#this is an alternative to 'fields'. You cannot have both 'fields' and
	 #'fieldsets'. 'fieldsets' basically groups fields however you like in a 
	 # detail page. 
	fieldsets = (
		#'None' and 'Add expiration date' are the titles of the fieldsets
		# for the admin page. 
		(None, {
			'fields': ('season', 'items', 'created_date')
			}),
		('Add expiration date', {
			'fields': ('expiration_date',),
			# classes: collapse is not necessary its just an extra feature
			# like a 'show more' type of thing to be applied to 
			# 'expiration_date'. 
			'classes': ('collapse',)
			})
		)



admin.site.register(Menu, MenuAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Ingredient)



