from django.contrib import admin
from .models import User, ChildParentsRelation, ClassName, Subject, ClassRoom, ClassSubject, StudentClass, ScheduleTemplate, Schedule, Holiday, Attendance


class AdminList(admin.ModelAdmin):
	def group(self, user):
		groups = []
		for group in user.groups.all():
			groups.append(group.name)
		return ' '.join(groups)

	group.short_description = 'Groups'

	list_display = ('username', 'email', 'first_name', 'last_name', 'group', 'is_active')
	list_filter = ('groups', 'is_staff', 'is_active')
	readonly_fields = ('last_login', 'date_joined',)


class ChildParent(admin.ModelAdmin):
	#def queryset(self, request):
		#students = User.objects.all().filter(groups__name='Student')
		#parents = list(User.objects.values("id", "first_name", "last_name").filter(groups__name="Parent"))
		#parents = User.objects.all().filter(groups__name='Parent')

	list_display = ('student', 'parent')


class ClassSubjectAdmin(admin.ModelAdmin):
	list_display = ('class_name', 'subject')


class StudentClassAdmin(admin.ModelAdmin):
	list_display = ('roll_no', 'session_year', 'student', 'class_name')


class ScheduleTemplateAdmin(admin.ModelAdmin):
	list_display = ('day', 'start_time', 'end_time', 'class_name', 'class_room', 'subject', 'teacher')


class ScheduleAdmin(admin.ModelAdmin):
	list_display = ('schedule_date', 'start_time', 'end_time', 'description', 'class_name', 'class_room', 'subject', 'teacher')

# for HolidayList
class HolidayList(admin.ModelAdmin):
	list_display = ('holiday_title', 'celebrate_on')
	ordering = ('celebrate_on', )

# for Attendance
class AttendanceAdmin(admin.ModelAdmin):
	list_display = ('present', 'student', 'schedule')


admin.site.unregister(User)
admin.site.register(User, AdminList)
admin.site.register(ChildParentsRelation, ChildParent)
admin.site.register(ClassName)
admin.site.register(Subject)
admin.site.register(ClassRoom)
admin.site.register(ClassSubject, ClassSubjectAdmin)
admin.site.register(StudentClass, StudentClassAdmin)
admin.site.register(ScheduleTemplate, ScheduleTemplateAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Holiday, HolidayList)
admin.site.register(Attendance, AttendanceAdmin)

