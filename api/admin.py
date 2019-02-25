from django.contrib import admin
from .models import User, Group,  ChildParentsRelation, ClassName, Subject, ClassRoom, Holiday



class adminList(admin.ModelAdmin):
	def group(self, user):
		groups = []
		for group in user.groups.all():
			groups.append(group.name)
		return ' '.join(groups)

	group.short_description = 'Groups'

	list_display = ('username', 'email', 'first_name', 'last_name', 'group', 'is_active')
	list_filter = ('groups','is_staff','is_active')
	readonly_fields = ('last_login', 'date_joined',)


class childParent(admin.ModelAdmin):

	def queryset(self, request):
		students = User.objects.all().filter(groups__name='Student')
		#parents = User.objects.all().filter(groups__name='Parent')


	list_display = ('student_id', 'parent_id')


class holidayList(admin.ModelAdmin):
	list_display = ('holiday_title','celebrate_on')
	ordering = ('celebrate_on',)


admin.site.unregister(User)
admin.site.register(User,adminList)
admin.site.register(ChildParentsRelation, childParent)
admin.site.register(ClassName)
admin.site.register(Subject)
admin.site.register(ClassRoom)
admin.site.register(Holiday, holidayList)

