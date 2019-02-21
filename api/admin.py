from django.contrib import admin
from .models import ChildParentsRelation, ClassName, Subject, ClassRoom

admin.site.register(ChildParentsRelation)
admin.site.register(ClassName)
admin.site.register(Subject)
admin.site.register(ClassRoom)
