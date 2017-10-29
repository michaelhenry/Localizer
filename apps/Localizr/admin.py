from django.contrib import admin

from .models import (
	UserInfoSavableModel,
	Locale,
	AppInfo,
	KeyString,
	AppInfoKeyString,
	LocalizedString,
	)

class UserInfoSavableAdmin(object):

	exclude = ('created_by', 'modified_by',)

	def save_model(self, request, obj, form, change):

		if not hasattr(obj, 'created_by'):
			obj.created_by = request.user
		obj.created_by = request.user
		obj.modified_by = request.user
		obj.save()

	def save_formset(self, request, form, formset, change): 
		
		objs = formset.save(commit=False)
		for obj in objs:
			if issubclass(obj.__class__, UserInfoSavableModel):
				if not hasattr(obj, 'created_by'):
					obj.created_by = request.user
				obj.modified_by = request.user
			obj.save()


class BaseModelAdmin(UserInfoSavableAdmin, admin.ModelAdmin):

	pass


class BaseTabularInlineModelAdmin(UserInfoSavableAdmin, admin.TabularInline):

	pass


class LocaleAdmin(BaseModelAdmin):

	ordering        =   ('name','code',)
	search_fields   =   ('name','code',)
	list_display    =   ('name' ,'code','description')
	

class AppInfoAdmin(BaseModelAdmin):

	fields          =   ('name', 'slug', 'description', 'base_locale',)
	ordering        =   ('name',)
	search_fields   =   ('name','description',)
	list_display    =   ('name', 'slug', 'description', 'base_locale')
	

class LocalizedStringInline(BaseTabularInlineModelAdmin):

	model = LocalizedString
	extra = 1


class KeyStringAdmin(BaseModelAdmin):

	ordering        =    ('key',)
	search_fields   =    ('key','description',)
	list_display    =    ('key' ,'description',)
	inlines         =    [LocalizedStringInline,]

	
class AppInfoKeyStringAdmin(BaseModelAdmin):

	fields              =    ('app_info', 'key_string',)
	ordering            =    ('app_info', 'key_string',)
	search_fields       =    ('key_string__key',)
	list_display        =    ('key_string' ,'app_info',)
	list_filter         =    ('app_info',)
	autocomplete_fields =    ['key_string', 'app_info']


class LocalizedStringAdmin(BaseModelAdmin):

	ordering            =    ('key_string', 'locale', 'value',)
	search_fields       =    ('key_string__key', 'value',)
	list_display        =    ('value', 'key_string', 'locale',)
	list_filter         =    ('locale',)
	autocomplete_fields =    ['key_string', 'locale']


admin.site.register(Locale, LocaleAdmin)
admin.site.register(AppInfo, AppInfoAdmin)
admin.site.register(KeyString, KeyStringAdmin)
admin.site.register(AppInfoKeyString, AppInfoKeyStringAdmin)
admin.site.register(LocalizedString, LocalizedStringAdmin)
admin.site.site_header = 'Localizr'