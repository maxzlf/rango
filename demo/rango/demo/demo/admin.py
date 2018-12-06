from django.contrib import admin
from .models import Student, Class



class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'gender', 'name',
                    'is_activated', 'create_time', 'update_time')
    ordering = ('-update_time',)


admin.site.register(Student, StudentAdmin)



class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_id', 'class_no', 'is_activated',
                    'create_time', 'update_time')
    ordering = ('-update_time',)


admin.site.register(Class, ClassAdmin)
